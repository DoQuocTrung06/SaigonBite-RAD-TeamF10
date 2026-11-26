using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    public class HubDAO
    {
        private static readonly Dictionary<string, Hub> _storage = new();

        public Hub? FindById(string hubId)
        {
            _storage.TryGetValue(hubId, out var hub);
            return hub;
        }

        public void Seed(Hub hub) => _storage[hub.HubId] = hub;

        public bool Update(Hub hub)
        {
            _storage[hub.HubId] = hub;
            return true;
        }
    }
}
