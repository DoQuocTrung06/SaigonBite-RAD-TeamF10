namespace SaigonBite.Domain
{
    public class KitchenTicket
    {
        public string TicketId { get; set; } = string.Empty;
        public string OrderId { get; set; } = string.Empty;
        public string StationId { get; set; } = string.Empty;
        public string Status { get; set; } = "QUEUED";
        public DateTime PrintedTime { get; set; } = DateTime.UtcNow;
        public DateTime? CompletedTime { get; set; }

        public void MarkCooking()
        {
            Status = "COOKING";
        }

        public void MarkReady()
        {
            Status = "READY";
            CompletedTime = DateTime.UtcNow;
        }
    }
}
