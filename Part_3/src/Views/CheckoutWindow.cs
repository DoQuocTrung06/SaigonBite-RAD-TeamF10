using SaigonBite.Controllers;

namespace SaigonBite.Views
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC3: Place an order
    public class CheckoutWindow
    {
        private readonly OrderHandler _handler;

        public CheckoutWindow(OrderHandler handler)
        {
            _handler = handler;
        }

        public string requestCheckout(List<Domain.MenuItem> basketItems)
        {
            string summary = _handler.requestCheckout(basketItems);
            Console.WriteLine($"[CheckoutWindow] {summary}");
            return summary;
        }

        public string enterDeliveryAddress(string deliveryAddress)
        {
            string summary = _handler.enterDeliveryAddress(deliveryAddress);
            Console.WriteLine($"[CheckoutWindow] {summary}");
            return summary;
        }

        public string applyVoucher(string voucherCode)
        {
            decimal updatedTotal = _handler.applyVoucher(voucherCode);
            var order = _handler.CurrentOrder;
            string msg = $"Voucher '{voucherCode}' applied -> Voucher Discount = {order.VoucherDiscountAmount:N0} VND, Total Discount = {order.DiscountAmount:N0} VND, Updated Total = {updatedTotal:N0} VND.";
            Console.WriteLine($"[CheckoutWindow] {msg}");
            return msg;
        }

        public string authorizeOnlinePayment(string paymentDetails)
        {
            string authCode = _handler.authorizeOnlinePayment(paymentDetails);
            string msg = $"Online payment authorized -> AuthCode = {authCode}.";
            Console.WriteLine($"[CheckoutWindow] {msg}");
            return msg;
        }

        public string submitOrder(string paymentMethod)
        {
            var order = _handler.submitOrder(paymentMethod);
            string receipt = $"Subtotal={order.Subtotal:N0} VND, DeliveryFee={order.DeliveryFee:N0} VND, Discount={order.DiscountAmount:N0} VND, FinalTotal={order.FinalTotal:N0} VND, Payment={order.OrderPayment?.PaymentStatus}, Tickets={order.Tickets.Count}";
            string eta = "25 mins";
            displayOrderReceipt(order.OrderId, receipt, eta);
            return order.OrderId;
        }

        public void displayOrderReceipt(string orderId, string receipt, string eta)
        {
            Console.WriteLine($"[CheckoutWindow] RECEIPT | Order #{orderId} | State: Placed | {receipt} | ETA: {eta}");
        }
    }
}
