namespace SaigonBite.Domain
{
    public abstract class Customer
    {
        public string CustomerId { get; set; } = string.Empty;
        public string FullName { get; set; } = string.Empty;
        public string CustomerType { get; set; } = string.Empty;
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }

    public class LocalCustomer : Customer
    {
        public string PhoneNumber { get; set; } = string.Empty;
        public LocalCustomer() { CustomerType = "Local"; }
    }

    public class ForeignTourist : Customer
    {
        public string PassportNumber { get; set; } = string.Empty;
        public string EmailAddress { get; set; } = string.Empty;
        public string PreferredLanguage { get; set; } = "en";
        public ForeignTourist() { CustomerType = "Foreign"; }
    }
}
