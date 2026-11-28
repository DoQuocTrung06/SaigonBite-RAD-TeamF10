using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    // Author: 524H0031 (Ngo Tan Thanh) - UC3: Place an order
    public class OrderDA
    {
        public static OrderDA Instance { get; } = new();
        private readonly Dictionary<string, Order> _orders = new(StringComparer.OrdinalIgnoreCase);
        private int _counter = 1;

        public string createOrder(Order order)
        {
            const string sqlInsertOrder = @"
                INSERT INTO orders (order_id, customer_id, hub_id, voucher_code, order_date_time, order_status,
                                    delivery_address, distance_km, subtotal, delivery_fee, discount_amount, final_total, payment_method)
                VALUES (@orderId, @customerId, @hubId, @voucherCode, @orderDateTime, 'Placed',
                        @deliveryAddress, @distanceKm, @subtotal, @deliveryFee, @discountAmount, @finalTotal, @paymentMethod);";
            const string sqlInsertLine = @"
                INSERT INTO order_lines (order_line_id, order_id, item_id, quantity, item_price, line_total, special_notes)
                VALUES (@lineId, @orderId, @itemId, @quantity, @itemPrice, @lineTotal, @specialNotes);";
            const string sqlInsertTicket = @"
                INSERT INTO kitchen_tickets (ticket_id, order_id, station_id, station_type, status, printed_time)
                VALUES (@ticketId, @orderId, @stationId, @stationType, 'Queued', CURRENT_TIMESTAMP);";
            _ = (sqlInsertOrder, sqlInsertLine, sqlInsertTicket);

            if (string.IsNullOrWhiteSpace(order.OrderId))
                order.OrderId = $"ORD-{_counter++:000}";

            _orders[order.OrderId] = order;
            return order.OrderId;
        }

        public Order? FindById(string orderId)
        {
            _orders.TryGetValue(orderId, out var order);
            return order;
        }

        public List<Order> GetAll() => _orders.Values.ToList();
    }
}
