module.exports = {
  name: "ChargeChase",
  description: "Recover failed payments automatically with branded dunning messages and secure billing portal integration.",
  version: "1.0.0",
  permissions: [
    "user:read",
    "company:read", 
    "webhook:write"
  ],
  pricing: {
    type: "transaction_fee",
    percentage: 2.9 // 2.9% of recovered revenue
  },
  paths: {
    app: "/experiences/[experienceId]",
    dashboard: "/dashboard/[companyId]",
    discover: "/discover"
  },
  webhooks: {
    enabled: true,
    events: ["payment.failed", "payment.succeeded"]
  },
  categories: ["payments", "automation", "analytics"],
  tags: ["stripe", "dunning", "revenue-recovery", "failed-payments"]
}