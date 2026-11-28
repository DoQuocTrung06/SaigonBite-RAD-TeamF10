namespace SaigonBite.Views
{
    public class VoucherConsoleUI
    {
        public void DisplayCreateResult(string code, bool success)
        {
            Console.WriteLine(success
                ? $"[VoucherConsoleUI] Voucher '{code}' persisted in Active status."
                : $"[VoucherConsoleUI] Failed to create voucher '{code}'.");
        }

        public void DisplayArchiveResult(string code, bool success)
        {
            Console.WriteLine(success
                ? $"[VoucherConsoleUI] Voucher '{code}' archived (soft deleted)."
                : $"[VoucherConsoleUI] Failed to archive voucher '{code}'.");
        }
    }
}
