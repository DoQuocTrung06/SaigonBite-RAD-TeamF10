using SaigonBite.Domain;
using SaigonBite.DataAccess;

namespace SaigonBite.Controllers
{
    public class ReportController
    {
        private readonly ReportDAO _reportDao;
        private readonly OrderDAO _orderDao;
        private readonly AuditLogDAO _auditDao;

        public ReportController(ReportDAO reportDao, OrderDAO orderDao, AuditLogDAO auditDao)
        {
            _reportDao = reportDao;
            _orderDao = orderDao;
            _auditDao = auditDao;
        }

        public ManagementReport GenerateReport(string hubId, DateTime start, DateTime end)
        {
            var orders = _orderDao.GetOrdersByHubAndDate(hubId, start, end);
            var reportId = $"REP_{hubId}_{DateTime.UtcNow:yyyyMMddHHmmss}";
            var report = new ManagementReport
            {
                ReportId = reportId,
                HubId = hubId,
                StartDate = start,
                EndDate = end
            };
            report.CalculateKPIs(orders, new List<DeliveryTask>());
            _reportDao.SaveReport(report);
            _auditDao.RecordAuditEntry(reportId, "HubManager", "GENERATE_MANAGEMENT_REPORT");
            return report;
        }

        public string ExportToPDF(string reportId)
        {
            _auditDao.RecordAuditEntry(reportId, "HubManager", "EXPORT_REPORT_PDF");
            return $"/exports/reports/{reportId}.pdf";
        }
    }
}
