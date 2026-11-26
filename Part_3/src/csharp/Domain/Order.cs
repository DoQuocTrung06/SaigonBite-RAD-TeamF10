namespace SaigonBite.Domain
{
    public class Order
    {
        public string OrderId { get; set; } = string.Empty;
        public string CustomerId { get; set; } = string.Empty;
        public string HubId { get; set; } = string.Empty;
        public string DeliveryAddress { get; set; } = string.Empty;
        public decimal DistanceKm { get; set; }
        public decimal Subtotal { get; set; }
        public decimal DeliveryFee { get; set; }
        public decimal DiscountAmount { get; set; }
        public decimal FinalTotal { get; set; }
        public string PaymentMethod { get; set; } = "COD";
        public string OrderStatus { get; set; } = "Ready_for_Pickup";
        public DateTime OrderTime { get; set; } = DateTime.UtcNow;
        public DateTime? DeliveredAt { get; set; }
        public string? CancellationReason { get; set; }
        public bool IsLocked { get; set; } = false;

        public void UpdateStatus(string newStatus, string? reason = null)
        {
            OrderStatus = newStatus;
            if (newStatus == "Confirmed") IsLocked = true;
            if (newStatus == "Delivered") DeliveredAt = DateTime.UtcNow;
            if (newStatus == "Delivery_Failed" || newStatus == "Cancelled" || newStatus == "Rejected") CancellationReason = reason;
        }
    }
}
