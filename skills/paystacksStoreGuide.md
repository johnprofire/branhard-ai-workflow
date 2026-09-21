# Paystack Storefront Guide

_Branhard / e-commerce build: checkout, webhook, and purchase alerts (email + SMS/WhatsApp)._


# Paystack Storefront Builder

Builds a storefront that takes payments through Paystack and pings the owner
(email + SMS/WhatsApp) the instant a purchase lands. Two things trip people up
every time, so read this before writing code:

1. **Paystack payment confirmation must happen server-side.** The frontend
   "payment successful" callback is not proof of payment — anyone can fake
   that browser event. Real confirmation comes from Paystack's webhook,
   verified with the *secret* key. This means a pure static site is not
   enough; there must be one small backend/serverless function.
2. **The purchase alert (email + SMS/WhatsApp) is triggered from that same
   webhook**, not from the frontend. That's what makes it trustworthy — you
   only get pinged for money that actually landed.

## Step 1 — Confirm the shape of the project

Don't guess; ask only what's missing, and only if it isn't already obvious
from context (an existing repo, prior conversation, uploaded files):

- Is this a new build or adding Paystack/alerts to an existing site?
- Where will it be hosted? (Vercel is the default assumption — a connector
  is often already available; ask before assuming another host.)
- Products: fixed catalog (hardcode/JSON) or does it need an admin/CMS?
- Email address and phone number (for WhatsApp/SMS) to send alerts to.

If the user has already answered these earlier in the conversation, don't
re-ask — proceed.

## Step 2 — Frontend

Default stack: React + Vite + Tailwind (matches most existing storefront
builds). Plain HTML/JS is fine for a simpler ask.

Use Paystack's **Inline JS (Popup)** for checkout — no backend call needed to
launch it, just a public key:

```html
<script src="https://js.paystack.co/v2/inline.js"></script>
```

See `assets/checkout-button.jsx` for a ready-to-drop React checkout button,
and `assets/checkout-button.html` for the plain-HTML/JS version. Both:
- Collect email + amount from the cart
- Open the Paystack popup with the **public** key (`pk_...` — safe in
  frontend code)
- On the popup's own success callback, just show "Payment received,
  confirming..." — never mark the order paid here, and never fire the email/
  SMS ping from this callback (see Step 1).

## Step 3 — Backend webhook (the part that actually confirms payment)

This is required, not optional. Build a small serverless function (Vercel
function, Netlify function, or a tiny Express server) at a route like
`/api/paystack-webhook`. Full working template: `references/webhook.md`.

The handler must:
1. Verify the request came from Paystack — HMAC-SHA512 of the raw body using
   the **secret** key (`sk_...`), compared to the `x-paystack-signature`
   header. Reject anything that doesn't match.
2. Check `event.event === "charge.success"`.
3. Only then: mark the order paid (in whatever storage the project uses) and
   fire the alerts (Step 4).
4. Respond `200` quickly — Paystack retries on non-200/timeout.

Register the webhook URL in the Paystack Dashboard → Settings → API Keys &
Webhooks, and set it before testing.

## Step 4 — Purchase alerts (email + SMS/WhatsApp)

Fire both from inside the verified webhook handler, in parallel:

- **Email**: Resend (simplest, generous free tier) or SMTP via Nodemailer.
  Template and code: `references/email-alert.md`.
- **SMS/WhatsApp**: Termii is the natural default for a Nigeria-based store
  (SMS + WhatsApp Business API, Nigerian routes, Naira billing). Twilio is
  the fallback if the user is targeting outside Nigeria or already has a
  Twilio account. Code for both: `references/sms-whatsapp-alert.md`.

Alert content should include: customer email, amount, product/reference, and
timestamp — the owner should be able to fulfill the order from the ping
alone.

## Step 5 — Environment variables checklist

Give the user this list explicitly — missing one is the most common failure:

```
PAYSTACK_SECRET_KEY      # sk_... — backend only, never in frontend code
PAYSTACK_PUBLIC_KEY      # pk_... — frontend, safe to expose
RESEND_API_KEY           # or SMTP_HOST/SMTP_USER/SMTP_PASS
OWNER_EMAIL
TERMII_API_KEY           # or TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN
OWNER_PHONE              # E.164 format, e.g. +234...
```

Never hardcode secret keys in code that gets committed — `.env` + add it to
`.gitignore`. If the user's repo has previously leaked a `.env`/`keys.env`
file, flag it and suggest rotating the keys in the Paystack dashboard.

## Step 6 — Ship it

- If a hosting connector (Vercel, etc.) is available in this session, offer
  to deploy directly and set the env vars there.
- Otherwise hand off the code as files, with a short README covering: install,
  env vars, `paystack webhook` URL registration, and how to test with
  Paystack's test-mode cards.
- Test-mode card for verifying the whole flow end-to-end before going live:
  `4084 0840 8408 4081`, any future expiry, CVV `408`, PIN `0000`, OTP
  `123456`.

## Reference files

- `references/webhook.md` — full webhook handler (Node/Express + Vercel
  serverless variants), signature verification code included
- `references/email-alert.md` — Resend and Nodemailer/SMTP code for the
  order-confirmation + owner-alert emails
- `references/sms-whatsapp-alert.md` — Termii and Twilio code for SMS and
  WhatsApp pings
- `assets/checkout-button.jsx` — React Paystack popup checkout button
- `assets/checkout-button.html` — plain HTML/JS version of the same

---

# Paystack Webhook Handler

This is the only place a purchase should ever be marked "paid" or trigger an
alert. Never trust the frontend success callback for this.

## Vercel serverless function

`api/paystack-webhook.js`:

```js
import crypto from "crypto";
import { sendPurchaseEmail } from "../lib/email.js";
import { sendPurchasePing } from "../lib/sms.js";

export const config = {
  api: { bodyParser: false }, // need the raw body for signature check
};

function getRawBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => (data += chunk));
    req.on("end", () => resolve(data));
    req.on("error", reject);
  });
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  const rawBody = await getRawBody(req);

  const expectedSignature = crypto
    .createHmac("sha512", process.env.PAYSTACK_SECRET_KEY)
    .update(rawBody)
    .digest("hex");

  if (expectedSignature !== req.headers["x-paystack-signature"]) {
    return res.status(401).send("Invalid signature");
  }

  const event = JSON.parse(rawBody);

  if (event.event === "charge.success") {
    const { customer, amount, reference, paid_at } = event.data;
    const order = {
      email: customer.email,
      amountNaira: amount / 100, // Paystack sends amount in kobo
      reference,
      paidAt: paid_at,
    };

    // TODO: mark the order as paid in your DB/storage here

    await Promise.all([
      sendPurchaseEmail(order),
      sendPurchasePing(order),
    ]);
  }

  // Always 200 quickly — Paystack retries on failure/timeout
  return res.status(200).send("ok");
}
```

## Plain Express server

```js
import express from "express";
import crypto from "crypto";
import { sendPurchaseEmail } from "./lib/email.js";
import { sendPurchasePing } from "./lib/sms.js";

const app = express();

// IMPORTANT: raw body needed for signature verification — mount this
// BEFORE any express.json() middleware, and only for this route.
app.post(
  "/api/paystack-webhook",
  express.raw({ type: "application/json" }),
  async (req, res) => {
    const expectedSignature = crypto
      .createHmac("sha512", process.env.PAYSTACK_SECRET_KEY)
      .update(req.body)
      .digest("hex");

    if (expectedSignature !== req.headers["x-paystack-signature"]) {
      return res.status(401).send("Invalid signature");
    }

    const event = JSON.parse(req.body);

    if (event.event === "charge.success") {
      const { customer, amount, reference, paid_at } = event.data;
      const order = {
        email: customer.email,
        amountNaira: amount / 100,
        reference,
        paidAt: paid_at,
      };

      // TODO: mark the order as paid in your DB/storage here

      await Promise.all([
        sendPurchaseEmail(order),
        sendPurchasePing(order),
      ]);
    }

    res.status(200).send("ok");
  }
);

app.listen(process.env.PORT || 3000);
```

## Registering the webhook

Paystack Dashboard → Settings → API Keys & Webhooks → Webhook URL →
`https://yourdomain.com/api/paystack-webhook`. Must be a publicly reachable
HTTPS URL (works with a Vercel preview/prod URL, or `ngrok` while developing
locally).

## Testing without a real payment

Paystack test mode lets you fully exercise the webhook using the test secret
key and this test card: `4084 0840 8408 4081`, any future expiry, CVV `408`,
PIN `0000`, OTP `123456`. Paystack also has a "Send Test Webhook" button in
the dashboard once the URL is registered.

---

# Purchase Email Alerts

Two options. Default to Resend unless the user already has Gmail/SMTP set up
or asks for it specifically.

## Option A — Resend (simplest)

```bash
npm install resend
```

`lib/email.js`:

```js
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendPurchaseEmail(order) {
  const { email, amountNaira, reference, paidAt } = order;

  // Alert to the store owner
  await resend.emails.send({
    from: "orders@yourdomain.com", // must be a domain verified in Resend
    to: process.env.OWNER_EMAIL,
    subject: `New order — ₦${amountNaira.toLocaleString()}`,
    html: `
      <p>New payment received.</p>
      <ul>
        <li>Customer: ${email}</li>
        <li>Amount: ₦${amountNaira.toLocaleString()}</li>
        <li>Reference: ${reference}</li>
        <li>Paid at: ${paidAt}</li>
      </ul>
    `,
  });

  // Confirmation to the customer
  await resend.emails.send({
    from: "orders@yourdomain.com",
    to: email,
    subject: "Order confirmed",
    html: `<p>Thanks for your order — reference <strong>${reference}</strong>. We'll be in touch with shipping details shortly.</p>`,
  });
}
```

Resend requires verifying a sending domain (DNS records) before you can send
from `orders@yourdomain.com` — until that's done, use their shared
`onboarding@resend.dev` sender for testing only.

## Option B — Nodemailer / SMTP (e.g. Gmail, Zoho, custom SMTP)

```bash
npm install nodemailer
```

```js
import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: 465,
  secure: true,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS, // use an app password, not the account password
  },
});

export async function sendPurchaseEmail(order) {
  const { email, amountNaira, reference, paidAt } = order;

  await transporter.sendMail({
    from: process.env.SMTP_USER,
    to: process.env.OWNER_EMAIL,
    subject: `New order — ₦${amountNaira.toLocaleString()}`,
    html: `<p>Customer: ${email}<br/>Amount: ₦${amountNaira.toLocaleString()}<br/>Reference: ${reference}<br/>Paid at: ${paidAt}</p>`,
  });

  await transporter.sendMail({
    from: process.env.SMTP_USER,
    to: email,
    subject: "Order confirmed",
    html: `<p>Thanks for your order — reference <strong>${reference}</strong>.</p>`,
  });
}
```

If using Gmail SMTP, the account needs an **app password** (2FA must be on
first) — a normal account password will be rejected.

---

# Purchase SMS / WhatsApp Alerts

Default to **Termii** for a Nigeria-based store — Nigerian routes, Naira
billing, and it covers both SMS and WhatsApp Business API from one account.
Use **Twilio** if the user is targeting outside Nigeria or already has a
Twilio account set up.

## Option A — Termii (SMS + WhatsApp)

```bash
npm install axios
```

```js
import axios from "axios";

const TERMII_BASE = "https://api.ng.termii.com/api";

export async function sendPurchasePing(order) {
  const { amountNaira, reference } = order;
  const message = `New order! ₦${amountNaira.toLocaleString()} — ref ${reference}`;

  // SMS
  await axios.post(`${TERMII_BASE}/sms/send`, {
    api_key: process.env.TERMII_API_KEY,
    to: process.env.OWNER_PHONE, // e.g. "234801XXXXXXX" (no + or leading 0)
    from: "Branhard",             // sender ID — must be registered with Termii first
    sms: message,
    type: "plain",
    channel: "generic",
  });

  // WhatsApp (requires WhatsApp enabled on the Termii account + an approved template)
  await axios.post(`${TERMII_BASE}/sms/whatsapp`, {
    api_key: process.env.TERMII_API_KEY,
    to: process.env.OWNER_PHONE,
    from: process.env.TERMII_WHATSAPP_SENDER_ID,
    sms: message,
    type: "plain",
    channel: "whatsapp",
  });
}
```

Sender IDs and WhatsApp templates need to be registered/approved in the
Termii dashboard before they'll send — this takes a day or two, so set it up
early rather than at launch.

## Option B — Twilio (SMS + WhatsApp)

```bash
npm install twilio
```

```js
import twilio from "twilio";

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

export async function sendPurchasePing(order) {
  const { amountNaira, reference } = order;
  const message = `New order! ₦${amountNaira.toLocaleString()} — ref ${reference}`;

  // SMS
  await client.messages.create({
    body: message,
    from: process.env.TWILIO_SMS_NUMBER, // your Twilio number, E.164 format
    to: process.env.OWNER_PHONE,          // E.164 format, e.g. +234...
  });

  // WhatsApp (needs the Twilio WhatsApp sandbox or an approved sender)
  await client.messages.create({
    body: message,
    from: `whatsapp:${process.env.TWILIO_WHATSAPP_NUMBER}`,
    to: `whatsapp:${process.env.OWNER_PHONE}`,
  });
}
```

Twilio's WhatsApp sandbox works instantly for testing but requires the
owner's phone to "join" the sandbox first by sending a code via WhatsApp; for
production, apply for an approved WhatsApp sender.

## Combining both channels in the webhook

`sendPurchasePing` above already fires SMS + WhatsApp together. Call it
alongside `sendPurchaseEmail` in `Promise.all(...)` from the webhook handler
so a slow SMS/WhatsApp API never blocks the email, and vice versa.

---

## Code assets

### React checkout button (`checkout-button.jsx`)
```jsx
// Drop into your cart/checkout page. Requires the Paystack inline script
// loaded once in index.html: <script src="https://js.paystack.co/v2/inline.js"></script>

import { useState } from "react";

export default function PaystackCheckoutButton({ email, amountNaira, onSuccess }) {
  const [loading, setLoading] = useState(false);

  const pay = () => {
    setLoading(true);
    const handler = window.PaystackPop.setup({
      key: import.meta.env.VITE_PAYSTACK_PUBLIC_KEY, // pk_... safe to expose
      email,
      amount: amountNaira * 100, // Paystack expects kobo
      currency: "NGN",
      callback: (response) => {
        setLoading(false);
        // This only confirms the popup closed successfully — the order is
        // NOT paid until the backend webhook verifies it server-side.
        onSuccess?.(response.reference);
      },
      onClose: () => setLoading(false),
    });
    handler.openIframe();
  };

  return (
    <button onClick={pay} disabled={loading}>
      {loading ? "Processing..." : `Pay ₦${amountNaira.toLocaleString()}`}
    </button>
  );
}
```

### Plain HTML/JS checkout button (`checkout-button.html`)
```html
<!-- Paste where the "Buy now" / checkout button should appear. -->
<script src="https://js.paystack.co/v2/inline.js"></script>

<button id="pay-btn">Pay now</button>

<script>
  document.getElementById("pay-btn").addEventListener("click", function () {
    var handler = PaystackPop.setup({
      key: "pk_..._your_public_key",
      email: "customer@example.com", // pull from your cart/checkout form
      amount: 500000, // amount in kobo — e.g. 500000 = ₦5,000
      currency: "NGN",
      callback: function (response) {
        // Popup succeeded — do NOT mark the order paid here.
        // The backend webhook is the source of truth (see references/webhook.md).
        alert("Payment received, confirming... ref: " + response.reference);
      },
      onClose: function () {
        console.log("Checkout closed");
      },
    });
    handler.openIframe();
  });
</script>
```
