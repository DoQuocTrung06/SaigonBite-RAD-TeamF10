using SaigonBite.Domain;
using SaigonBite.DataAccess;

namespace SaigonBite.Controllers
{
    public class DeliveryController
    {
        private readonly DeliveryTaskDAO _taskDao;
        private readonly OrderDAO _orderDao;
        private readonly AuditLogDAO _auditDao;

        public DeliveryController(DeliveryTaskDAO taskDao, OrderDAO orderDao, AuditLogDAO auditDao)
        {
            _taskDao = taskDao;
            _orderDao = orderDao;
            _auditDao = auditDao;
        }

        public bool ProcessPickupScan(string orderId, string qrCode)
        {
            var task = _taskDao.FindByOrderId(orderId);
            if (task == null) return false;

            task.UpdatePickupStatus(DateTime.UtcNow);
            _taskDao.Update(task);
            _orderDao.UpdateStatus(orderId, "Out_for_Delivery");
            _auditDao.RecordAuditEntry(orderId, "Shipper", "SCAN_PICKUP_SUCCESS");
            return true;
        }

        public bool RecordDeliverySuccess(string orderId, decimal codAmount, string photoUrl)
        {
            var task = _taskDao.FindByOrderId(orderId);
            var order = _orderDao.FindById(orderId);
            if (task == null || order == null) return false;

            if (order.PaymentMethod == "COD")
            {
                var payment = new Payment { PaymentId = $"PAY_{orderId}", OrderId = orderId, PaymentAmount = order.FinalTotal };
                payment.ConfirmCODPayment(codAmount);
            }

            task.CompleteDelivery(codAmount, photoUrl);
            _taskDao.Update(task);
            _orderDao.UpdateStatus(orderId, "Delivered");
            _auditDao.RecordAuditEntry(orderId, "Shipper", "DELIVERY_SUCCESS_COD_RECONCILED");
            return true;
        }

        public bool RecordDeliveryFailure(string orderId, string reason, string photoUrl)
        {
            var task = _taskDao.FindByOrderId(orderId);
            if (task == null) return false;

            task.MarkFailed(reason, photoUrl);
            _taskDao.Update(task);
            _orderDao.UpdateStatus(orderId, "Delivery_Failed", reason);
            _auditDao.RecordAuditEntry(orderId, "Shipper", "DELIVERY_FAILED_10MIN_TIMEOUT");
            return true;
        }
    }
}
