namespace SaigonBite.Domain
{
    // Authors: 524H0031 (UC3), 524H0132 (UC7)
    public class KitchenTicket
    {
        private static int _counter = 1;

        public string TicketId { get; set; } = string.Empty;
        public string OrderId { get; set; } = string.Empty;
        public string StationId { get; set; } = string.Empty;
        public string StationType { get; set; } = "Wok";
        public string Status { get; set; } = "Queued";
        public DateTime PrintedTime { get; set; } = DateTime.UtcNow;
        public DateTime? CompletedTime { get; set; }

        // UC3 (524H0031): Queue preparation ticket for specialized kitchen station (Wok, Fryer, Assembly, Beverage)
        public KitchenTicket createStationTicket(string stationType)
        {
            TicketId = $"KT-{_counter++:000}";
            StationType = stationType;
            StationId = $"ST-H01-{stationType.ToUpperInvariant()}";
            Status = "Queued";
            PrintedTime = DateTime.UtcNow;
            return this;
        }

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
