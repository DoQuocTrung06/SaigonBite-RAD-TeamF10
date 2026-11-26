using SaigonBite.Domain;
using SaigonBite.DataAccess;

namespace SaigonBite.Controllers
{
    public class VoucherController
    {
        private readonly VoucherDAO _voucherDao;
        private readonly AuditLogDAO _auditDao;

        public VoucherController(VoucherDAO voucherDao, AuditLogDAO auditDao)
        {
            _voucherDao = voucherDao;
            _auditDao = auditDao;
        }

        public bool CreateVoucher(string code, decimal discountPercent, decimal maxDiscount, decimal minOrder, DateTime start, DateTime end, int quota)
        {
            if (_voucherDao.FindByCode(code) != null) return false;

            var voucher = new Voucher
            {
                VoucherCode = code,
                DiscountPercent = discountPercent,
                MaxDiscountAmount = maxDiscount,
                MinOrderAmount = minOrder,
                StartDate = start,
                EndDate = end,
                UsageQuota = quota,
                Status = start <= DateTime.UtcNow ? "Active" : "Scheduled"
            };

            if (!voucher.Validate()) return false;

            _voucherDao.Save(voucher);
            _auditDao.RecordAuditEntry(code, "Administrator", "CREATE_VOUCHER");
            return true;
        }

        public bool UpdateVoucherQuota(string code, int newQuota)
        {
            var voucher = _voucherDao.FindByCode(code);
            if (voucher == null || newQuota <= 0) return false;

            voucher.UpdateQuota(newQuota);
            _voucherDao.Update(voucher);
            _auditDao.RecordAuditEntry(code, "Administrator", "UPDATE_VOUCHER_QUOTA");
            return true;
        }

        public bool ArchiveVoucher(string code)
        {
            var voucher = _voucherDao.FindByCode(code);
            if (voucher == null) return false;

            voucher.Archive();
            _voucherDao.Update(voucher);
            _auditDao.RecordAuditEntry(code, "Administrator", "ARCHIVE_VOUCHER");
            return true;
        }
    }
}
