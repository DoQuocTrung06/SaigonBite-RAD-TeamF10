using SaigonBite.Domain;

namespace SaigonBite.DataAccess
{
    public class ReportDAO
    {
        private static readonly Dictionary<string, ManagementReport> _storage = new();

        public bool SaveReport(ManagementReport report)
        {
            _storage[report.ReportId] = report;
            return true;
        }

        public ManagementReport? FindReportById(string reportId)
        {
            _storage.TryGetValue(reportId, out var report);
            return report;
        }
    }
}
