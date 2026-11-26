namespace SaigonBite.Domain
{
    public class Voucher
    {
        public string VoucherCode { get; set; } = string.Empty;
        public decimal DiscountPercent { get; set; }
        public decimal MaxDiscountAmount { get; set; }
        public decimal MinOrderAmount { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public int UsageQuota { get; set; }
        public int UsedCount { get; set; }
        public string Status { get; set; } = "Scheduled";

        public bool Validate()
        {
            return !string.IsNullOrWhiteSpace(VoucherCode)
                && DiscountPercent > 0 && DiscountPercent <= 100
                && MaxDiscountAmount > 0
                && MinOrderAmount >= 0
                && EndDate > StartDate
                && UsageQuota > 0;
        }

        public void UpdateQuota(int newQuota)
        {
            if (newQuota > 0)
            {
                UsageQuota = newQuota;
                if (Status == "Depleted" && UsedCount < UsageQuota)
                {
                    Status = "Active";
                }
            }
        }

        public void Archive()
        {
            Status = "Archived";
        }
    }
}
