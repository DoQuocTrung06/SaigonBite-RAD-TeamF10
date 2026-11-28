namespace SaigonBite.DataAccess
{
    public class AuditLogDAO
    {
        public bool RecordAuditEntry(string orderId, string actor, string action)
        {
            Console.WriteLine($"[AUDIT LOG] {DateTime.UtcNow:s} | Entity: {orderId} | Actor: {actor} | Action: {action}");
            return true;
        }
    }
}
