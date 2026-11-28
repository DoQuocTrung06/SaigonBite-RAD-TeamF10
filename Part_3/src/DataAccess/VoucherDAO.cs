using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    public class VoucherDAO
    {
        private static readonly Dictionary<string, Voucher> _storage = new();

        public Voucher? FindByCode(string voucherCode)
        {
            _storage.TryGetValue(voucherCode, out var voucher);
            return voucher;
        }

        public bool Save(Voucher voucher)
        {
            _storage[voucher.VoucherCode] = voucher;
            return true;
        }

        public bool Update(Voucher voucher)
        {
            if (!_storage.ContainsKey(voucher.VoucherCode)) return false;
            _storage[voucher.VoucherCode] = voucher;
            return true;
        }

        public List<Voucher> GetAll() => _storage.Values.ToList();
    }
}
