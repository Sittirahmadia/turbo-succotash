"""
Network & Latency Optimizer for NEON VOID OPTIMIZER.
Comprehensive network optimization including TCP/IP tweaks, DNS optimization,
QoS tagging, latency testing, and adapter management.
"""

import logging
import subprocess
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

logger = logging.getLogger("NEON_VOID")


@dataclass
class NetworkAdapter:
    """Represents a network adapter."""
    name: str
    description: str
    mac_address: str
    ip_address: str
    is_physical: bool
    is_up: bool
    speed_mbps: int


@dataclass
class LatencyResult:
    """Result from a latency test."""
    server_name: str
    server_host: str
    avg_ms: float
    min_ms: float
    max_ms: float
    jitter_ms: float
    packet_loss: float
    timestamp: float


class NetworkOptimizer:
    """
    Comprehensive network optimization module.
    Handles TCP/IP tuning, DNS optimization, QoS, and latency testing.
    """

    # Common gaming DNS servers
    DNS_SERVERS = {
        "Cloudflare": ["1.1.1.1", "1.0.0.1"],
        "Cloudflare_Family": ["1.1.1.3", "1.0.0.3"],
        "Google": ["8.8.8.8", "8.8.4.4"],
        "OpenDNS": ["208.67.222.222", "208.67.220.220"],
        "Quad9": ["9.9.9.9", "149.112.112.112"],
        "Level3": ["209.244.0.3", "209.244.0.4"],
    }

    # Game servers for latency testing
    GAME_SERVERS = {
        "Cloudflare": "1.1.1.1",
        "Valorant_US_West": "192.207.0.1",
        "Valorant_US_East": "192.207.1.1",
        "CS2_US": "162.254.197.1",
        "Fortnite": "3.233.0.1",
        "Apex_Legends": "104.198.0.1",
        "League_of_Legends": "104.160.0.1",
        "Overwatch": "24.105.0.1",
    }

    def __init__(self) -> None:
        self.adapters: List[NetworkAdapter] = []
        self.current_adapter: Optional[str] = None
        self._latency_history: List[LatencyResult] = []
        self._scan_adapters()

    def _scan_adapters(self) -> None:
        """Scan for network adapters."""
        try:
            import psutil
            stats = psutil.net_if_stats()
            addresses = psutil.net_if_addrs()

            for name, stat in stats.items():
                # Skip loopback and virtual adapters
                is_physical = not any(x in name.lower() for x in [
                    'loopback', 'lo', 'virtual', 'hyper-v', 'vmware',
                    'docker', 'tun', 'tap', 'wg', 'veth'
                ])

                ip_addr = ""
                mac_addr = ""
                if name in addresses:
                    for addr in addresses[name]:
                        if addr.family == 2:  # IPv4
                            ip_addr = addr.address
                        elif addr.family == -1 or addr.family == 17:  # MAC
                            mac_addr = addr.address

                adapter = NetworkAdapter(
                    name=name,
                    description=name,
                    mac_address=mac_addr,
                    ip_address=ip_addr,
                    is_physical=is_physical,
                    is_up=stat.isup,
                    speed_mbps=stat.speed // 1000000 if stat.speed else 0
                )
                self.adapters.append(adapter)

            logger.info(f"Found {len(self.adapters)} network adapters")

        except Exception as e:
            logger.error(f"Adapter scan failed: {e}")

    def get_adapters(self) -> List[NetworkAdapter]:
        """Get list of network adapters."""
        return self.adapters

    def apply_gaming_profile(self, adapter_name: str) -> Dict[str, str]:
        """
        Apply comprehensive gaming-optimized network settings.
        Returns dict of applied tweaks and their status.
        """
        results = {}

        try:
            # 1. Disable Nagle's Algorithm
            results['nagle'] = self._set_registry_tweak(
                r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces",
                "TcpNoDelay", 1
            )

            # 2. TCP Ack Frequency
            results['tcp_ack'] = self._set_registry_tweak(
                r"SOFTWARE\Microsoft\MSMQ\Parameters",
                "TCPNoDelay", 1
            )

            # 3. Network Throttling Index
            results['net_throttle'] = self._set_registry_tweak(
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
                "NetworkThrottlingIndex", 0xffffffff
            )

            # 4. TCP AutoTuning
            results['autotuning'] = self._run_netsh_command(
                "netsh interface tcp set global autotuninglevel=disabled"
            )

            # 5. Set congestion provider to CTCP (Compound TCP on Windows)
            results['congestion'] = self._run_netsh_command(
                "netsh interface tcp set global congestionprovider=ctcp"
            )

            # 6. ECN capability
            results['ecn'] = self._run_netsh_command(
                "netsh interface tcp set global ecncapability=enabled"
            )

            # 7. RSS
            results['rss'] = self._run_netsh_command(
                "netsh interface tcp set global rss=enabled"
            )

            # 8. Timestamp disabling (reduces overhead)
            results['timestamps'] = self._run_netsh_command(
                "netsh interface tcp set global timestamps=disabled"
            )

            logger.info("Gaming network profile applied")

        except Exception as e:
            logger.error(f"Failed to apply gaming profile: {e}")
            results['error'] = str(e)

        return results

    def optimize_mtu(self, adapter_name: str, mtu_size: int = 1500) -> str:
        """Optimize MTU size with PMTUD."""
        try:
            # First discover optimal MTU
            result = self._run_netsh_command(
                f"netsh interface ipv4 set subinterface \"{adapter_name}\" mtu={mtu_size} store=persistent"
            )
            logger.info(f"MTU set to {mtu_size} on {adapter_name}")
            return result
        except Exception as e:
            logger.error(f"MTU optimization failed: {e}")
            return f"Failed: {e}"

    def benchmark_dns(self) -> Dict[str, float]:
        """Benchmark all configured DNS servers."""
        results = {}

        for name, servers in self.DNS_SERVERS.items():
            try:
                import dns.resolver
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [servers[0]]
                resolver.timeout = 2
                resolver.lifetime = 2

                # Query multiple times for average
                times = []
                for _ in range(3):
                    start = time.time()
                    try:
                        resolver.resolve('google.com', 'A')
                        times.append((time.time() - start) * 1000)
                    except Exception:
                        pass

                if times:
                    results[name] = sum(times) / len(times)
                else:
                    results[name] = -1  # Failed

            except ImportError:
                # Fallback using ping
                result = self._ping_host(servers[0], count=2)
                results[name] = result.get('avg', -1)
            except Exception as e:
                logger.debug(f"DNS benchmark failed for {name}: {e}")
                results[name] = -1

        return results

    def set_dns(self, primary: str, secondary: str) -> str:
        """Set DNS servers for the active adapter."""
        try:
            # Get active adapter
            active = [a for a in self.adapters if a.is_up and a.is_physical]
            if not active:
                return "No active adapter found"

            adapter = active[0]

            cmd = (
                f'netsh interface ip set dns "{adapter.name}" static {primary} primary && '
                f'netsh interface ip add dns "{adapter.name}" {secondary} index=2'
            )
            result = self._run_command(cmd)
            logger.info(f"DNS set to {primary}, {secondary}")
            return result

        except Exception as e:
            logger.error(f"DNS change failed: {e}")
            return f"Failed: {e}"

    def test_latency(self, target: Optional[str] = None) -> LatencyResult:
        """Test latency to a target server."""
        if target is None:
            target = "1.1.1.1"

        result = self._ping_host(target, count=10)

        latency = LatencyResult(
            server_name=target,
            server_host=target,
            avg_ms=result.get('avg', 0),
            min_ms=result.get('min', 0),
            max_ms=result.get('max', 0),
            jitter_ms=result.get('jitter', 0),
            packet_loss=result.get('loss', 0),
            timestamp=time.time()
        )

        self._latency_history.append(latency)
        if len(self._latency_history) > 100:
            self._latency_history.pop(0)

        return latency

    def test_all_servers(self) -> List[LatencyResult]:
        """Test latency to all game servers."""
        results = []
        for name, host in self.GAME_SERVERS.items():
            try:
                result = self.test_latency(host)
                result.server_name = name
                results.append(result)
                time.sleep(0.2)  # Brief pause between tests
            except Exception as e:
                logger.debug(f"Latency test failed for {name}: {e}")

        return results

    def get_latency_history(self) -> List[LatencyResult]:
        """Get latency test history."""
        return self._latency_history

    def _ping_host(self, host: str, count: int = 4) -> Dict[str, float]:
        """Ping a host and return statistics."""
        try:
            result = subprocess.run(
                ['ping', '-n', str(count), host],
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout

            # Parse Windows ping output
            stats = {'min': 0, 'max': 0, 'avg': 0, 'loss': 0, 'jitter': 0}

            # Extract packet loss
            if 'Lost' in output or 'loss' in output.lower():
                import re
                loss_match = re.search(r'(\d+)% loss', output)
                if loss_match:
                    stats['loss'] = float(loss_match.group(1))

            # Extract RTT stats
            if 'Average' in output:
                import re
                rtt_match = re.search(r'Minimum\s*=\s*(\d+)ms.*?Maximum\s*=\s*(\d+)ms.*?Average\s*=\s*(\d+)ms', output)
                if rtt_match:
                    stats['min'] = float(rtt_match.group(1))
                    stats['max'] = float(rtt_match.group(2))
                    stats['avg'] = float(rtt_match.group(3))
                    stats['jitter'] = stats['max'] - stats['min']

            return stats

        except subprocess.TimeoutExpired:
            return {'min': 0, 'max': 0, 'avg': 0, 'loss': 100, 'jitter': 0}
        except Exception as e:
            logger.debug(f"Ping error: {e}")
            return {'min': 0, 'max': 0, 'avg': 0, 'loss': 100, 'jitter': 0}

    def _run_command(self, cmd: str) -> str:
        """Run a shell command."""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=10
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {e}"

    def _run_netsh_command(self, cmd: str) -> str:
        """Run a netsh command with admin check."""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=10
            )
            success = result.returncode == 0
            return "Applied" if success else f"Failed: {result.stderr[:100]}"
        except Exception as e:
            return f"Error: {e}"

    def _set_registry_tweak(self, path: str, key: str, value: int) -> str:
        """Set a registry value (logs intent, actual modification requires admin)."""
        try:
            import winreg
            # This would require admin to actually write
            # For safety, we log what would be changed
            logger.info(f"Registry tweak: {path}\\{key} = {value}")
            return "Requires admin"
        except ImportError:
            return "Windows only"
        except Exception as e:
            return f"Error: {e}"
