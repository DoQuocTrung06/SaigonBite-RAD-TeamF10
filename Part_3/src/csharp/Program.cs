using SaigonBite.Controllers;
using SaigonBite.DataAccess;
using SaigonBite.Domain;
using SaigonBite.Views;

namespace SaigonBite
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var voucherDao = new VoucherDAO();
            var orderDao = new OrderDAO();
            var ticketDao = new KitchenTicketDAO();
            var hubDao = new HubDAO();
            var auditDao = new AuditLogDAO();

            var voucherController = new VoucherController(voucherDao, auditDao);
            var kitchenController = new KitchenController(orderDao, ticketDao, hubDao, auditDao);
            var voucherUi = new VoucherConsoleUI();
            var kdsUi = new KDSConsoleUI();

            hubDao.Seed(new Hub { HubId = "H01", HubName = "District 1 Hub", MaxCapacityOrders = 50, CurrentActiveOrders = 20 });
            hubDao.Seed(new Hub { HubId = "H02", HubName = "District 7 Hub", MaxCapacityOrders = 40, CurrentActiveOrders = 35 });

            orderDao.Seed(new Order { OrderId = "ORD-001", CustomerId = "CUS-01", HubId = "H01", FinalTotal = 187500m, PaymentMethod = "Card", OrderStatus = "Pending_Kitchen" });
            orderDao.Seed(new Order { OrderId = "ORD-002", CustomerId = "CUS-02", HubId = "H02", FinalTotal = 165000m, PaymentMethod = "COD", OrderStatus = "Pending_Kitchen" });

            Console.WriteLine("=== SAIGONBITE PART 3 LIVE DEMO (524H0132 - UC15 & UC7) ===");

            // TC_UC15_01: Create active voucher
            bool tc15 = voucherController.CreateVoucher("QUIET10", 10m, 40000m, 100000m, DateTime.UtcNow.AddDays(-1), DateTime.UtcNow.AddDays(30), 200);
            voucherUi.DisplayCreateResult("QUIET10", tc15);
            Console.WriteLine($"TC_UC15_01: {(tc15 && voucherDao.FindByCode("QUIET10")?.Status == "Active" ? "PASS" : "FAIL")}");

            // TC_UC7_01: Confirm incoming order within 120s SLA
            bool tc7Confirm = kitchenController.ConfirmOrder("ORD-001", "ST-H01-GRILL", 45);
            var ord1 = orderDao.FindById("ORD-001");
            kdsUi.DisplayOrderConfirmation("ORD-001", tc7Confirm, ord1?.IsLocked ?? false);
            Console.WriteLine($"TC_UC7_01: {(tc7Confirm && ord1?.OrderStatus == "Confirmed" && ord1.IsLocked && ticketDao.FindByOrderId("ORD-001").Count == 1 ? "PASS" : "FAIL")}");

            // TC_UC7_02: Reject incoming order with reason & trigger refund
            bool tc7Reject = kitchenController.RejectOrder("ORD-002", "Out of Beef Pho");
            var ord2 = orderDao.FindById("ORD-002");
            kdsUi.DisplayOrderRejection("ORD-002", ord2?.CancellationReason ?? string.Empty, tc7Reject);
            Console.WriteLine($"TC_UC7_02: {(tc7Reject && ord2?.OrderStatus == "Cancelled" && ord2.CancellationReason == "Out of Beef Pho" ? "PASS" : "FAIL")}");
        }
    }
}
