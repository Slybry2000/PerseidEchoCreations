const path = require("path");
const express = require("express");
const nodemailer = require("nodemailer");
require("dotenv").config();

const app = express();

const PORT = Number(process.env.PORT || 3000);
const MAIL_TO = process.env.MAIL_TO || "Bryan@perseidechocreations.com";
const SMTP_HOST = process.env.SMTP_HOST || "";
const SMTP_PORT = Number(process.env.SMTP_PORT || 587);
const SMTP_SECURE =
    String(process.env.SMTP_SECURE || "").toLowerCase() === "true" || SMTP_PORT === 465;
const SMTP_USER = process.env.SMTP_USER || "";
const SMTP_PASS = process.env.SMTP_PASS || "";
const SMTP_FROM = process.env.SMTP_FROM || SMTP_USER || MAIL_TO;

app.use(express.json({ limit: "50kb" }));
app.use(express.urlencoded({ extended: false }));

const transporter =
    SMTP_HOST && SMTP_USER && SMTP_PASS
        ? nodemailer.createTransport({
              host: SMTP_HOST,
              port: SMTP_PORT,
              secure: SMTP_SECURE,
              auth: {
                  user: SMTP_USER,
                  pass: SMTP_PASS
              }
          })
        : null;

function clean(value) {
    return String(value || "").trim();
}

function isEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function isConfigured() {
    return Boolean(transporter && SMTP_FROM && MAIL_TO);
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

app.get("/api/health", (req, res) => {
    res.json({
        ok: true,
        mailConfigured: isConfigured()
    });
});

app.post("/api/quote-request", async (req, res) => {
    if (!isConfigured()) {
        return res.status(503).json({
            ok: false,
            message: "Quote endpoint is not configured. Set SMTP environment variables."
        });
    }

    const name = clean(req.body.name);
    const email = clean(req.body.email);
    const company = clean(req.body.company) || "Not provided";
    const appType = clean(req.body.appType);
    const budget = clean(req.body.budget);
    const timeline = clean(req.body.timeline);
    const summary = clean(req.body.summary);

    if (!name || !email || !appType || !budget || !timeline || !summary) {
        return res.status(400).json({
            ok: false,
            message: "Please complete all required fields."
        });
    }

    if (!isEmail(email)) {
        return res.status(400).json({
            ok: false,
            message: "Please enter a valid email."
        });
    }

    const textBody = [
        "New app quote request",
        "",
        `Name: ${name}`,
        `Email: ${email}`,
        `Company: ${company}`,
        `App type: ${appType}`,
        `Budget: ${budget}`,
        `Timeline: ${timeline}`,
        "",
        "Project summary:",
        summary
    ].join("\n");

    const htmlBody = `
        <h2>New app quote request</h2>
        <p><strong>Name:</strong> ${escapeHtml(name)}</p>
        <p><strong>Email:</strong> ${escapeHtml(email)}</p>
        <p><strong>Company:</strong> ${escapeHtml(company)}</p>
        <p><strong>App type:</strong> ${escapeHtml(appType)}</p>
        <p><strong>Budget:</strong> ${escapeHtml(budget)}</p>
        <p><strong>Timeline:</strong> ${escapeHtml(timeline)}</p>
        <p><strong>Project summary:</strong><br>${escapeHtml(summary).replace(/\n/g, "<br>")}</p>
    `;

    try {
        await transporter.sendMail({
            from: SMTP_FROM,
            to: MAIL_TO,
            replyTo: email,
            subject: `App quote request from ${name}`,
            text: textBody,
            html: htmlBody
        });

        return res.json({ ok: true });
    } catch (error) {
        console.error("Quote email send failed:", error);
        return res.status(500).json({
            ok: false,
            message: "We could not send your request. Please try again shortly."
        });
    }
});

app.use(express.static(path.resolve(__dirname)));

app.get("*", (req, res, next) => {
    if (req.path.startsWith("/api/")) {
        return next();
    }
    return res.sendFile(path.resolve(__dirname, "index.html"));
});

app.use((req, res) => {
    if (req.path.startsWith("/api/")) {
        return res.status(404).json({ ok: false, message: "Not found" });
    }
    return res.status(404).send("Not found");
});

function startServer(port = PORT) {
    return app.listen(port, () => {
        console.log(`PEC website server listening on http://localhost:${port}`);
    });
}

if (require.main === module) {
    startServer();
}

module.exports = { app, startServer };
