
import AppKit
import WebKit

final class AppDelegate: NSObject, NSApplicationDelegate, WKNavigationDelegate {
    var window: NSWindow!
    var web: WKWebView!

    func applicationDidFinishLaunching(_ n: Notification) {
        NSApp.setActivationPolicy(.regular)
        let rect = NSRect(x: 0, y: 0, width: 1180, height: 820)
        window = NSWindow(contentRect: rect,
                          styleMask: [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView],
                          backing: .buffered, defer: false)
        window.title = "命題データベース — Forb-LT 1.8"
        window.titlebarAppearsTransparent = false
        window.appearance = NSAppearance(named: .aqua)
        window.minSize = NSSize(width: 720, height: 480)

        let cfg = WKWebViewConfiguration()
        web = WKWebView(frame: rect, configuration: cfg)
        web.autoresizingMask = [.width, .height]
        window.contentView = web
        window.center()

        if let url = Bundle.main.url(forResource: "index", withExtension: "html") {
            web.loadFileURL(url, allowingReadAccessTo: url.deletingLastPathComponent())
        }
        web.navigationDelegate = self
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
        buildMenu()
    }

    func buildMenu() {
        let m = NSMenu()
        let appItem = NSMenuItem(); m.addItem(appItem)
        let appMenu = NSMenu()
        appMenu.addItem(withTitle: "命題データベースについて", action: #selector(NSApplication.orderFrontStandardAboutPanel(_:)), keyEquivalent: "")
        appMenu.addItem(.separator())
        appMenu.addItem(withTitle: "隠す", action: #selector(NSApplication.hide(_:)), keyEquivalent: "h")
        appMenu.addItem(withTitle: "終了", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        appItem.submenu = appMenu

        let editItem = NSMenuItem(); m.addItem(editItem)
        let edit = NSMenu(title: "編集")
        edit.addItem(withTitle: "コピー", action: #selector(NSText.copy(_:)), keyEquivalent: "c")
        edit.addItem(withTitle: "すべて選択", action: #selector(NSText.selectAll(_:)), keyEquivalent: "a")
        editItem.submenu = edit

        let viewItem = NSMenuItem(); m.addItem(viewItem)
        let view = NSMenu(title: "表示")
        view.addItem(withTitle: "検索", action: #selector(focusSearch), keyEquivalent: "f")
        view.addItem(withTitle: "再読み込み", action: #selector(reload), keyEquivalent: "r")
        viewItem.submenu = view
        NSApp.mainMenu = m
    }

    @objc func focusSearch() {
        web.evaluateJavaScript("(()=>{const q=document.getElementById('q');q.focus();q.select();})()", completionHandler: nil)
    }
    @objc func reload() { web.reload() }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        webView.evaluateJavaScript("document.title + '|' + document.querySelectorAll('.item').length + '|' + document.getElementById('count').textContent") { v, e in
            let s = "loaded: \(v ?? "nil") err: \(e.map { "\($0)" } ?? "none")"
            try? s.write(toFile: "/tmp/forblt_loaded.txt", atomically: true, encoding: .utf8)
        }
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ s: NSApplication) -> Bool { true }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.run()
