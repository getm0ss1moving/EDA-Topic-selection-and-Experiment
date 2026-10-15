import Foundation
import PDFKit

// Print the text layer of a PDF, page by page. Reading aid only.
let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let doc = PDFDocument(url: url) else {
    print("OPEN_FAIL")
    exit(1)
}
for i in 0..<doc.pageCount {
    if let page = doc.page(at: i) {
        print("=== PAGE \(i + 1) ===")
        print(page.string ?? "")
    }
}
