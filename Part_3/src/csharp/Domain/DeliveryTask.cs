namespace SaigonBite.Domain
{
    public class DeliveryTask
    {
        public string TaskId { get; set; } = string.Empty;
        public string OrderId { get; set; } = string.Empty;
        public string ShipperId { get; set; } = string.Empty;
        public DateTime? PickupTime { get; set; }
        public DateTime? DeliveredTime { get; set; }
        public string DeliveryStatus { get; set; } = "Assigned";
        public decimal CashCollected { get; set; }
        public string? FailureReason { get; set; }
        public string? ProofPhotoUrl { get; set; }

        public void UpdatePickupStatus(DateTime timestamp)
        {
            DeliveryStatus = "Picked_Up";
            PickupTime = timestamp;
        }

        public void CompleteDelivery(decimal codAmount, string photoUrl)
        {
            DeliveryStatus = "Delivered";
            DeliveredTime = DateTime.UtcNow;
            CashCollected = codAmount;
            ProofPhotoUrl = photoUrl;
        }

        public void MarkFailed(string reason, string photoUrl)
        {
            DeliveryStatus = "Failed_Returned";
            DeliveredTime = DateTime.UtcNow;
            FailureReason = reason;
            ProofPhotoUrl = photoUrl;
        }
    }
}
