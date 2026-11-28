using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    public class KitchenTicketDAO
    {
        private static readonly Dictionary<string, KitchenTicket> _storage = new();

        public bool Save(KitchenTicket ticket)
        {
            _storage[ticket.TicketId] = ticket;
            return true;
        }

        public List<KitchenTicket> FindByOrderId(string orderId)
        {
            return _storage.Values.Where(t => t.OrderId == orderId).ToList();
        }

        public List<KitchenTicket> GetAll() => _storage.Values.ToList();
    }
}
