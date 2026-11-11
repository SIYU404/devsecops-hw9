"""系統健康檢查與連線診斷工具.

本模組提供基礎的網路連線可用性檢查功能，
並將診斷結果格式化為監控日誌。
"""

import subprocess  # nosec B404


def check_host_status(hostname: str) -> bool:
    """使用系統 ping 指令檢查指定主機是否在線上.

    修復說明：
    1. 將指令拆解為串列（List），避免字串拼接。
    2. 移除 shell=True，徹底防範命令注入漏洞。
    3. 加入 try-except 機制處理指令執行時的系統例外狀況。
    """
    command = ["ping", "-n", "1", hostname]
    try:
        # nosec 標記表示此處已使用安全 list 參數，排除 S603 誤判
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )  # nosec B603
        return result.returncode == 0
    except OSError:
        return False


def format_health_report(service_name: str, is_healthy: bool) -> str:
    """格式化指定服務的健康檢查報告文字.

    修復說明：
    1. 補齊運算符號前後的標準空格。
    2. 使用 f-string 取代舊式字串加號拼接。
    """
    status_text = "UP" if is_healthy else "DOWN"
    return f"Service [{service_name}] is currently: {status_text}"


def main() -> None:
    """執行主要的診斷工作流程."""
    target_host = "8.8.8.8"
    print("Starting system health check...")

    is_up = check_host_status(target_host)
    report = format_health_report("DNS_Service", is_up)
    print(report)


if __name__ == "__main__":
    main()
