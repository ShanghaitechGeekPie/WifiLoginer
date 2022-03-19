//
//  ViewController.swift
//  SHTLogin
//
//  Created by Zian He on 2022/3/16.
//
import UIKit
import WebKit
import SystemConfiguration

class ViewController: UIViewController, WKUIDelegate {
    struct DefaultsKeys {
        static let name = "name"
        static let pass = "pass"
    }
    var flg = 0
    
    @IBOutlet weak var username: UITextField!
    @IBOutlet weak var password: UITextField!
    @IBOutlet weak var label: UILabel!
    
    @IBOutlet weak var web1: WKWebView!
    
    @IBAction func reload(_ sender: Any) {
        label.text=""
        loadweb()
    }
    @IBAction func connect(_ sender: Any) {
        log()
    }
    @IBAction func check(_ sender: Any) {
        if currentReachabilityStatus == .notReachable {
            label.text="网络未连接"
            //print("网络未连接")
            // Network Unavailable
        } else {
            label.text="网络已连接"
            //print("网络已连接")
            // Network Available
        }
    }
    
    @IBAction func save(_ sender: Any) {
        let defaults = UserDefaults.standard
        let n1 = (username.text! as NSString)
        let p1 = (password.text! as NSString)
        defaults.set(n1, forKey: DefaultsKeys.name)
        defaults.set(p1, forKey: DefaultsKeys.pass)
        flg = 1
    }
    // 点击屏幕收起键盘
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        
        view.endEditing(true)
        
    }
    
    override func motionEnded(_ motion: UIEvent.EventSubtype, with event: UIEvent?) {
        log()
    }
    
    func log(){
        if flg == 1{
            if (!web1.isLoading) {
                let defaults = UserDefaults.standard
                let name1 = (defaults.string(forKey: DefaultsKeys.name)! as NSString)
                let pass1 = (defaults.string(forKey: DefaultsKeys.pass)! as NSString)
                web1.evaluateJavaScript("document.getElementById('username').value='\(name1)';")
                web1.evaluateJavaScript("document.getElementById('password').value='\(pass1)';")
                let jsString = "document.getElementById('loginBtn').click()"
                web1.evaluateJavaScript(jsString)}}
        else{
            let jsString = "document.getElementById('loginBtn').click()"
            web1.evaluateJavaScript(jsString)
        }
        }
    func loadweb(){
        let myURL = URL(string:"https://controller.shanghaitech.edu.cn:8445/PortalServer/customize/1478262836414/phone/auth.jsp")
        let myRequest = URLRequest(url: myURL!)
        web1.load(myRequest)
        
        let defaults = UserDefaults.standard
        if (!DefaultsKeys.name.isEmpty) && (!DefaultsKeys.pass.isEmpty){
            let name1 = defaults.string(forKey: DefaultsKeys.name)
            let pass1 = defaults.string(forKey: DefaultsKeys.pass)
            username.text = name1
            password.text = pass1
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        loadweb()
    }
}

protocol Utilities {}
extension NSObject: Utilities {
    enum ReachabilityStatus {
        case notReachable
        case reachableViaWWAN
        case reachableViaWiFi
    }
    
    var currentReachabilityStatus: ReachabilityStatus {
        
        var zeroAddress = sockaddr_in()
        zeroAddress.sin_len = UInt8(MemoryLayout<sockaddr_in>.size)
        zeroAddress.sin_family = sa_family_t(AF_INET)
        guard let defaultRouteReachability = withUnsafePointer(to: &zeroAddress, {
            $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
                SCNetworkReachabilityCreateWithAddress(nil, $0)
            }
        }) else {
            return .notReachable
        }
        
        var flags: SCNetworkReachabilityFlags = []
        if !SCNetworkReachabilityGetFlags(defaultRouteReachability, &flags) {
            return .notReachable
        }
        
        if flags.contains(.reachable) == false {
            // The target host is not reachable.
            return .notReachable
        }
        else if flags.contains(.isWWAN) == true {
            // WWAN connections are OK if the calling application is using the CFNetwork APIs.
            return .reachableViaWWAN
        }
        else if flags.contains(.connectionRequired) == false {
            // If the target host is reachable and no connection is required then we'll assume that you're on Wi-Fi...
            return .reachableViaWiFi
        }
        else if (flags.contains(.connectionOnDemand) == true || flags.contains(.connectionOnTraffic) == true) && flags.contains(.interventionRequired) == false {
            // The connection is on-demand (or on-traffic) if the calling application is using the CFSocketStream or higher APIs and no [user] intervention is needed
            return .reachableViaWiFi
        }
        else {
            return .notReachable
        }
    }
}

