using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC3: Place an order
    public class VoucherDA
    {
        public static VoucherDA Instance { get; } = new();
        private readonly Dictionary<string, Voucher> _vouchers = new(StringComparer.OrdinalIgnoreCase);

        public Voucher? readVoucher(string voucherCode)
        {
            const string sql = "SELECT * FROM vouchers WHERE voucher_code = @voucherCode;";
            _ = sql;
            if (string.IsNullOrWhiteSpace(voucherCode)) return null;
            _vouchers.TryGetValue(voucherCode, out var voucher);
            return voucher;
        }

        public bool updateVoucher(Voucher voucher)
        {
            const string sql = "UPDATE vouchers SET usage_quota = @usageQuota, used_count = used_count + 1 WHERE voucher_code = @voucherCode;";
            _ = sql;
            _vouchers[voucher.VoucherCode] = voucher;
            return true;
        }

        public void SeedVoucher(Voucher voucher)
        {
            _vouchers[voucher.VoucherCode] = voucher;
        }
    }
}
