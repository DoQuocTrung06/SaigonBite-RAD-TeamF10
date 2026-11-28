using SaigonBite.Domain;
using SaigonBite.DataAccess;

namespace SaigonBite.Controllers
{
    public class KitchenController
    {
        private readonly OrderDAO _orderDao;
        private readonly KitchenTicketDAO _ticketDao;
        private readonly HubDAO _hubDao;
        private readonly AuditLogDAO _auditDao;

        public KitchenController(OrderDAO orderDao, KitchenTicketDAO ticketDao, HubDAO hubDao, AuditLogDAO auditDao)
        {
            _orderDao = orderDao;
            _ticketDao = ticketDao;
            _hubDao = hubDao;
            _auditDao = auditDao;
        }

        public bool ConfirmOrder(string orderId, string stationId, int elapsedSeconds)
        {
            var order = _orderDao.FindById(orderId);
            if (order == null || order.OrderStatus != "Pending_Kitchen") return false;

            if (elapsedSeconds > 120)
            {
                _orderDao.UpdateStatus(orderId, "Cancelled", "120-second kitchen confirmation SLA timeout");
                _auditDao.RecordAuditEntry(orderId, "System", "ORDER_TIMEOUT_REFUND_TRIGGERED");
                return false;
            }

            var hub = _hubDao.FindById(order.HubId);
            if (hub != null && hub.IsOverloaded())
            {
                _hubDao.Update(hub);
                _auditDao.RecordAuditEntry(hub.HubId, "KitchenController", "HUB_BUSY_THRESHOLD_85_REACHED");
            }

            _orderDao.UpdateStatus(orderId, "Confirmed");
            if (hub != null)
            {
                hub.CurrentActiveOrders++;
                hub.IsOverloaded();
                _hubDao.Update(hub);
            }

            var ticket = new KitchenTicket
            {
                TicketId = $"KT_{orderId}",
                OrderId = orderId,
                StationId = stationId,
                Status = "COOKING"
            };
            _ticketDao.Save(ticket);
            _auditDao.RecordAuditEntry(orderId, "KitchenStaff", "ORDER_CONFIRMED_AND_LOCKED");
            return true;
        }

        public bool RejectOrder(string orderId, string reason)
        {
            if (string.IsNullOrWhiteSpace(reason)) return false;

            var order = _orderDao.FindById(orderId);
            if (order == null || order.OrderStatus != "Pending_Kitchen") return false;

            _orderDao.UpdateStatus(orderId, "Cancelled", reason);
            _auditDao.RecordAuditEntry(orderId, "KitchenStaff", $"ORDER_REJECTED_REFUND_TRIGGERED: {reason}");
            return true;
        }
    }
}
