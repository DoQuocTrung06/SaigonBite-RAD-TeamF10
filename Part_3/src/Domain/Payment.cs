using SaigonBite.DataAccess;

namespace SaigonBite.Domain
{
    // Authors: 524H0031 (UC3), 524H0136 (UC10)
    public class Payment
    {
        public string PaymentId { get; set; } = string.Empty;
        public string OrderId { get; set; } = string.Empty;
        public string PaymentMethod { get; set; } = "Cash on Delivery";
        public decimal PaymentAmount { get; set; }
        public string PaymentStatus { get; set; } = "Unpaid";
        public string AuthorizationCode { get; set; } = string.Empty;
        public DateTime PaymentDateTime { get; set; } = DateTime.UtcNow;

        // UC3 (524H0031): Authorize online payment via Payment Gateway (Exception 4.1a on declined card)
        public string authorizeOnlinePayment(string paymentDetails, decimal amount)
        {
            if (string.IsNullOrWhiteSpace(paymentDetails)
                || paymentDetails.Contains("DECLINED", StringComparison.OrdinalIgnoreCase))
            {
                PaymentStatus = "Declined";
                throw new InvalidOperationException("4.1a Online payment authorization declined by Payment Gateway.");
            }

            PaymentAmount = amount;
            PaymentMethod = "Online Payment";
            PaymentStatus = "Paid";
            AuthorizationCode = $"AUTH-{DateTime.UtcNow:yyyyMMdd}-{Math.Abs(paymentDetails.GetHashCode()) % 9000 + 1000}";
            PaymentDateTime = DateTime.UtcNow;
            return AuthorizationCode;
        }

        // UC3 (524H0031): Record payment as Paid (Online Payment) or Unpaid (Cash on Delivery in VND)
        public Payment recordPayment(string paymentMethod, decimal amount)
        {
            if (string.IsNullOrWhiteSpace(PaymentId))
                PaymentId = $"PAY-{DateTime.UtcNow:HHmmss}-{Random.Shared.Next(100, 999)}";

            PaymentMethod = paymentMethod;
            PaymentAmount = amount;
            PaymentDateTime = DateTime.UtcNow;

            if (paymentMethod.Contains("Online", StringComparison.OrdinalIgnoreCase)
                || paymentMethod.Contains("Card", StringComparison.OrdinalIgnoreCase))
            {
                PaymentStatus = "Paid";
                if (string.IsNullOrWhiteSpace(AuthorizationCode))
                    AuthorizationCode = $"AUTH-{DateTime.UtcNow:yyyyMMdd}-1024";
            }
            else
            {
                PaymentStatus = "Unpaid"; // COD settled in VND upon delivery (A-04)
                AuthorizationCode = string.Empty;
            }

            PaymentDA.Instance.createPayment(this);
            return this;
        }

        public bool ConfirmCODPayment(decimal collectedAmount)
        {
            if (collectedAmount < PaymentAmount)
                throw new ArgumentException("Insufficient COD cash collected.");
            PaymentStatus = "Paid";
            return true;
        }
    }
}
