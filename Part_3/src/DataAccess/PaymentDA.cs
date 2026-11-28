using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC3: Place an order
    public class PaymentDA
    {
        public static PaymentDA Instance { get; } = new();
        private readonly Dictionary<string, Payment> _payments = new(StringComparer.OrdinalIgnoreCase);

        public bool createPayment(Payment payment)
        {
            const string sql = @"
                INSERT INTO payments (payment_id, order_id, payment_method, payment_amount, payment_status, authorization_code, payment_date_time)
                VALUES (@paymentId, @orderId, @paymentMethod, @paymentAmount, @paymentStatus, @authorizationCode, CURRENT_TIMESTAMP);";
            _ = sql;
            _payments[payment.PaymentId] = payment;
            return true;
        }

        public Payment? FindByOrderId(string orderId)
        {
            return _payments.Values.FirstOrDefault(p => p.OrderId == orderId);
        }
    }
}
