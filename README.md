# IT 222 Network Automation Group Assignment

## 1. Assignment Identification

- **Course:** IT 222
- **Assignment Number:** Assignment 16
- **Scenario:** Microfinance Institution Network
- **Group Number:** Group 15

## 2. Group Members

| S/N | Name | Registration Number |
|-----|------|----------------------|
| 1 | Goodluck Audiface Sunga | 2024/0342 |
| 2 | Kaiza Zakayo Sanga | 2024/1547 |
| 3 | Elizabeth Renatus Mbuga | 2024/1534 |
| 4 | Hamza Madua Mikidadi | 2024/1830 |

## 3. Scenario Description

The assigned organization is a microfinance institution operating two offices. Each office
handles two distinct categories of staff: Tellers, who process customer deposits,
withdrawals, and loan repayments at the counter, and Loan Officers, who assess, approve,
and manage customer loan accounts. Because Teller transactions and Loan Officer systems
serve different operational functions and carry different sensitivity levels, they must be
logically separated on the network. At the same time, both offices belong to the same
institution and must remain connected so that Teller-to-Teller and Loan-Officer-to-Loan-Officer
communication is possible between the two locations.

## 4. Network Requirements

The network must:

- keep Teller traffic and Loan Officer traffic in separate VLANs at each office;
- provide each VLAN with a router-based gateway using router-on-a-stick inter-VLAN
  routing;
- carry both VLANs correctly across an 802.1Q trunk between each switch and its router;
- connect the two offices over a routed link between R1 and R2;
- use OSPF to dynamically exchange routes between the two offices, so that Tellers at one
  office can reach Tellers at the other office, and Loan Officers at one office can reach
  Loan Officers at the other office.

## 5. Topology Description

- **R1** — Site A (Office 1) router. Provides router-on-a-stick inter-VLAN routing for the
  Teller and Loan Officer VLANs at Site A, and connects to R2 over the routed link.
- **R2** — Site B (Office 2) router. Mirrors R1's role for Site B.
- **SW1** — Site A switch. Hosts the Teller and Loan Officer access ports and trunks both
  VLANs to R1.
- **SW2** — Site B switch. Mirrors SW1's role for Site B.
- **End devices** — Teller-PC1 and LoanOfficer-PC1 at Site A; Teller-PC2 and
  LoanOfficer-PC2 at Site B.
- **Router-to-switch trunks** — SW1 Gi0/1 to R1 Gi0/0, and SW2 Gi0/1 to R2 Gi0/0, both
  configured as 802.1Q trunks carrying VLAN 61 and VLAN 71.
- **R1–R2 link** — a routed point-to-point link running OSPF, connecting the two offices.

## 6. Network Addressing and VLANs

| VLAN ID | VLAN Name | Site A Subnet | Site B Subnet |
|---------|-----------|----------------|----------------|
| 61 | Tellers | 192.168.61.0/24 | 192.168.161.0/24 |
| 71 | LoanOfficers | 192.168.71.0/24 | 192.168.171.0/24 |

| Device | Interface | VLAN | Address |
|--------|-----------|------|---------|
| R1 | Gi0/0.61 | 61 Tellers | 192.168.61.1/24 |
| R1 | Gi0/0.71 | 71 LoanOfficers | 192.168.71.1/24 |
| R1 | Gi0/1 | — | 10.16.16.1/30 |
| R2 | Gi0/0.61 | 61 Tellers | 192.168.161.1/24 |
| R2 | Gi0/0.71 | 71 LoanOfficers | 192.168.171.1/24 |
| R2 | Gi0/1 | — | 10.16.16.2/30 |
| SW1 | Gi0/1 | Trunk | Allow 61,71 |
| SW1 | Gi0/2 | 61 | Teller-PC1 → 192.168.61.10/24 |
| SW1 | Gi0/3 | 71 | LoanOfficer-PC1 → 192.168.71.10/24 |
| SW2 | Gi0/1 | Trunk | Allow 61,71 |
| SW2 | Gi0/2 | 61 | Teller-PC2 → 192.168.161.10/24 |
| SW2 | Gi0/3 | 71 | LoanOfficer-PC2 → 192.168.171.10/24 |

Router link: 10.16.16.0/30 (R1 = 10.16.16.1, R2 = 10.16.16.2)

## 7. Routing Method

The network uses **OSPF, process 1, area 0**, running between R1 and R2. OSPF was chosen
(as specified by the assigned scenario) over static routing because it allows the two
offices to automatically learn and adjust to each other's Teller and LoanOfficer subnets
without the group having to hand-enter and maintain routes on both routers. This matters
operationally for a microfinance institution because Teller and Loan Officer connectivity
between offices needs to keep working reliably as the network is verified and tested,
without a static route being missed or left inconsistent between R1 and R2.

## 8. Scenario Requirements Analysis

| Scenario Requirement | Configuration | Verification | Test |
|-----------------------|----------------|----------------|------|
| Separate Teller and Loan Officer traffic at each office | VLAN 61 and VLAN 71 created on SW1/SW2; Teller and Loan Officer PCs assigned to the correct access ports | `show vlan brief`, `show interfaces status` | Confirm each PC lands in the correct VLAN and reaches its own gateway |
| Carry both VLANs to the router | 802.1Q trunk on SW1 Gi0/1 and SW2 Gi0/1 | `show interfaces trunk` | Confirm both VLANs are carried and reach R1/R2 |
| Route between Teller and Loan Officer VLANs locally | Router subinterfaces Gi0/0.61 and Gi0/0.71 on R1 and R2 | `show ip interface brief`, `show ip route` | Local inter-VLAN reachability at each site |
| Connect the two offices | Routed R1–R2 link at 10.16.16.0/30, OSPF process 1 area 0 | `show ip ospf neighbor`, `show ip route` | R1 ↔ R2 ping; Teller-PC1 ↔ Teller-PC2; LoanOfficer-PC1 ↔ LoanOfficer-PC2 |

## 9. Configuration Strategy

- **r1_config.py / r2_config.py** configure the hostname, bring up the physical trunk
  interface, create the Teller (VLAN 61) and LoanOfficer (VLAN 71) subinterfaces with
  802.1Q encapsulation and IP addressing, bring up the routed R1–R2 link, and enable OSPF
  process 1 area 0 for the local VLAN subnets and the link subnet.
- **sw1_config.py / sw2_config.py** configure the hostname, create VLAN 61 (Tellers) and
  VLAN 71 (LoanOfficers), assign the two access ports to their respective VLANs, and
  configure the uplink port as an 802.1Q trunk allowing both VLANs through to the router.
- There is no separate network-level configuration script; the network is fully configured
  through the four device-level configuration scripts above.

## 10. Verification Strategy

- **r1_verify.py / r2_verify.py** check `show ip interface brief` to confirm subinterface
  addressing and interface state, `show running-config` to confirm the applied
  configuration, `show ip route` to confirm routes are present, and
  `show ip ospf neighbor` to confirm that R1 and R2 have formed a full OSPF adjacency over
  the routed link — this last check matters because a working ping does not by itself
  prove that OSPF (as opposed to some other mechanism) is what is providing reachability.
- **sw1_verify.py / sw2_verify.py** check `show vlan brief` to confirm both VLANs exist
  and the correct ports are assigned, `show interfaces status` to confirm access ports are
  up, `show interfaces trunk` to confirm the trunk is carrying VLAN 61 and 71, and
  `show mac address-table` to confirm the switch has learned the connected PCs.
- **network_verify.py** runs the router and switch verification commands above against
  all four devices from a single script, giving one consolidated view that the VLANs,
  trunks, subinterfaces, and OSPF adjacency are all correctly in place across the
  integrated network.

## 11. Testing Strategy

| Test | Source | Destination | Purpose | Expected Result |
|------|--------|-------------|---------|-------------------|
| R1–R2 link reachability | R1 | 10.16.16.2 | Confirm the routed inter-office link is up before testing anything that depends on it | Ping succeeds |
| Teller inter-office communication | Teller-PC1 (Site A) | Teller-PC2 (192.168.161.10, Site B) | Confirm Tellers at one office can reach Tellers at the other office, as required by the scenario | Ping succeeds |
| Loan Officer inter-office communication | LoanOfficer-PC1 (Site A) | LoanOfficer-PC2 (192.168.171.10, Site B) | Confirm Loan Officers at one office can reach Loan Officers at the other office, as required by the scenario | Ping succeeds |

`network_test.py` runs all three tests above from a single script. A successful ping in
each case is treated as evidence that the corresponding VLAN, trunk, router subinterface,
routed link, and OSPF-learned route are all functioning together correctly for that
specific business function, not simply that "the network can ping."

## 12. How to Run the Scripts

1. Open the GNS3 project and start all devices: R1, R2, SW1, SW2, and PC1–PC4.
2. In GNS3's Topology Summary panel, note the current TELNET console port assigned to
   each device, since these can change whenever the project is saved or reopened.
3. Open each script (`r1_config.py`, `r2_config.py`, `sw1_config.py`, `sw2_config.py`,
   `r1_verify.py`, `r2_verify.py`, `sw1_verify.py`, `sw2_verify.py`, `r1_test.py`,
   `r2_test.py`, `sw1_test.py`, `sw2_test.py`, `network_verify.py`, `network_test.py`)
   and update the `host` and `port` values to match the current GNS3 VM IP address and
   the TELNET ports noted above.
4. Run the configuration scripts in this order: `sw1_config.py`, `sw2_config.py`,
   `r1_config.py`, `r2_config.py`.
5. On each PC console in GNS3, manually set the PC's IP address and gateway using the
   VPCS `ip` command, then save it with `save`.
6. Run the verification scripts in any order: `r1_verify.py`, `r2_verify.py`,
   `sw1_verify.py`, `sw2_verify.py`, or run `network_verify.py` to check all four devices
   in one pass.
7. Run the testing scripts: `r1_test.py`, `r2_test.py`, `sw1_test.py`, `sw2_test.py`, or
   run `network_test.py` to run the scenario-based end-to-end tests in one pass.

## 13. Expected Results

Once configuration is applied, verification should show VLAN 61 and VLAN 71 present on
both switches with the correct access ports, both VLANs carried across both trunks, both
routers holding the correct subinterface addressing, and R1 and R2 forming a full OSPF
neighbor adjacency over the 10.16.16.0/30 link. Testing should show successful pings
between R1 and R2, between the two Teller PCs across offices, and between the two Loan
Officer PCs across offices, confirming that both business functions of the microfinance
institution are correctly connected between Site A and Site B.

## 14. Assumptions or Additional Features

- `show ip ospf neighbor` was added to the router verification and network-level
  verification scripts beyond the base template, since a static-routing-style check of
  `show ip route` alone does not demonstrate that OSPF neighbor formation is actually
  working.
- End devices are named Teller-PC1, LoanOfficer-PC1 (Site A) and Teller-PC2,
  LoanOfficer-PC2 (Site B) to reflect their role in the microfinance scenario.
- `network_test.py` currently tests connectivity from Site A to Site B (Teller-PC1 and
  LoanOfficer-PC1 as sources). Testing in the reverse direction from Teller-PC2 and
  LoanOfficer-PC2 was not included as a separate source group.
- No additional access-control or security feature beyond the base VLAN/OSPF requirements
  of the scenario was implemented.
