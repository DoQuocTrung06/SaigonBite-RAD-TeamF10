using SaigonBite.Controllers;

namespace SaigonBite.Views
{
    public class ShipperMobileUI
    {
        private readonly DeliveryController _controller;

        public ShipperMobileUI(DeliveryController controller)
        {
            _controller = controller;
        }

        public void DisplayAssignedTrip(string tripDetails) => Console.WriteLine($"[UI] Trip: {tripDetails}");
        public bool OnScanPickupQRClicked(string orderId, string qr) => _controller.ProcessPickupScan(orderId, qr);
        public bool OnConfirmDeliveryClicked(string orderId, decimal cod, string photo) => _controller.RecordDeliverySuccess(orderId, cod, photo);
        public bool OnReportFailureClicked(string orderId, string reason, string photo) => _controller.RecordDeliveryFailure(orderId, reason, photo);
    }
}
