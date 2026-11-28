namespace SaigonBite.Domain
{
    public class Payment
    {
        public string PaymentId { get; set; } = string.Empty;
        public string OrderId { get; set; } = string.Empty;
        public decimal PaymentAmount { get; set; }
        public string PaymentStatus { get; set; } = "PENDING";

        public bool ConfirmCODPayment(decimal collectedAmount)
        {
            if (collectedAmount < PaymentAmount)
                throw new ArgumentException("Insufficient COD cash collected.");
            PaymentStatus = "SUCCESS";
            return true;
        }
    }
}
