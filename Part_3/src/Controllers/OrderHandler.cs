using SaigonBite.Domain;

namespace SaigonBite.Controllers
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC3: Place an order
    public class OrderHandler
    {
        private Hub _activeHub = new();
        private Order _activeOrder = new();

        public Order CurrentOrder => _activeOrder;
        public Hub CurrentHub => _activeHub;

        public string requestCheckout(List<MenuItem> basketItems)
        {
            _activeHub = new Hub();
            _activeOrder = new Order();

            _activeHub.verifyHubCapacity(basketItems);

            foreach (var item in basketItems)
            {
                _activeOrder.addOrderLine(item, 1, "Standard preparation");
            }

            decimal subtotal = _activeOrder.calculateSubtotal();
            return $"Checkout initialized at {_activeHub.HubName} ({_activeHub.HubId}): {basketItems.Count} items, Subtotal = {subtotal:N0} VND.";
        }

        public string enterDeliveryAddress(string deliveryAddress)
        {
            decimal distanceKm = _activeHub.calculateDistance(deliveryAddress);
            bool quietEligible = _activeHub.checkQuietKitchenDiscount();
            decimal total = _activeOrder.calculateDeliveryAndTotal(deliveryAddress, distanceKm, quietEligible);

            return $"Distance = {distanceKm:F1} km | Delivery Fee = {_activeOrder.DeliveryFee:N0} VND | Quiet-Kitchen 10% = {_activeOrder.QuietDiscountAmount:N0} VND | Payable = {total:N0} VND.";
        }

        public decimal applyVoucher(string voucherCode)
        {
            return _activeOrder.applyVoucherDiscount(voucherCode);
        }

        public string authorizeOnlinePayment(string paymentDetails)
        {
            return _activeOrder.authorizePayment(paymentDetails);
        }

        public Order submitOrder(string paymentMethod)
        {
            _activeOrder.completeOrder(paymentMethod);
            return _activeOrder;
        }
    }
}
