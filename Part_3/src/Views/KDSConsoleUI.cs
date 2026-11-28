namespace SaigonBite.Views
{
    public class KDSConsoleUI
    {
        public void DisplayOrderConfirmation(string orderId, bool confirmed, bool locked)
        {
            Console.WriteLine(confirmed
                ? $"[KDSConsoleUI] Order '{orderId}' CONFIRMED. Address & items locked: {locked}."
                : $"[KDSConsoleUI] Order '{orderId}' could not be confirmed.");
        }

        public void DisplayOrderRejection(string orderId, string reason, bool rejected)
        {
            Console.WriteLine(rejected
                ? $"[KDSConsoleUI] Order '{orderId}' REJECTED (Reason: {reason}). Refund triggered."
                : $"[KDSConsoleUI] Order '{orderId}' rejection failed.");
        }
    }
}
