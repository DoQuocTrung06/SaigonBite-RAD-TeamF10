using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    public class OrderDAO
    {
        private static readonly Dictionary<string, Order> _storage = new();

        public Order? FindById(string orderId)
        {
            _storage.TryGetValue(orderId, out var order);
            return order;
        }

        public bool UpdateStatus(string orderId, string status, string? reason = null)
        {
            if (_storage.TryGetValue(orderId, out var order))
            {
                order.UpdateStatus(status, reason);
                return true;
            }
            return false;
        }

        public List<Order> GetOrdersByHubAndDate(string hubId, DateTime start, DateTime end)
        {
            return _storage.Values
                .Where(o => o.HubId == hubId && o.OrderTime >= start && o.OrderTime <= end)
                .ToList();
        }

        public void Seed(Order order) => _storage[order.OrderId] = order;
    }
}
