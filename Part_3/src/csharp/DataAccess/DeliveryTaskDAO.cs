using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    public class DeliveryTaskDAO
    {
        private static readonly Dictionary<string, DeliveryTask> _storage = new();

        public DeliveryTask? FindByOrderId(string orderId)
        {
            return _storage.Values.FirstOrDefault(t => t.OrderId == orderId);
        }

        public bool Update(DeliveryTask task)
        {
            _storage[task.TaskId] = task;
            return true;
        }

        public void Seed(DeliveryTask task) => _storage[task.TaskId] = task;
    }
}
