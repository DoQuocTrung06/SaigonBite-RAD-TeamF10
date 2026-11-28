using SaigonBite.DataAccess;

namespace SaigonBite.Domain
{
    // Authors: 524H0031 (UC3), 524H0132 (UC15)
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

        // UC3 (524H0031): Calculate promotional voucher discount without blocking checkout on invalid code (Exception 3.1a)
        public decimal calculateDiscount(string voucherCode, decimal subtotal)
        {
            var v = VoucherDA.Instance.readVoucher(voucherCode);
            if (v == null || !v.Status.Equals("Active", StringComparison.OrdinalIgnoreCase))
                return 0m;
            if (DateTime.UtcNow < v.StartDate || DateTime.UtcNow > v.EndDate)
                return 0m;
            if (v.UsedCount >= v.UsageQuota || subtotal < v.MinOrderAmount)
                return 0m;

            decimal raw = Math.Round(subtotal * (v.DiscountPercent / 100m), 0);
            return v.MaxDiscountAmount > 0 ? Math.Min(raw, v.MaxDiscountAmount) : raw;
        }

        // UC3 (524H0031): Increment voucher usage count and persist via VoucherDA
        public void redeemVoucher()
        {
            UsedCount++;
            if (UsedCount >= UsageQuota)
                Status = "Depleted";
            VoucherDA.Instance.updateVoucher(this);
        }

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
