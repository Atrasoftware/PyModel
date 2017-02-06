cases = [
 ('PowerOn, PowerOff alternate due to enabling conditions',
  'pmt -n 10 OrchidCncPistonDisp'),

 ('PowerOn, PowerOff alternate, end in non-accepting state',
  'pmt -n 3 OrchidCncPistonDisp'),

 ('Same as above but add -c cleanup option to reach accepting state',
  'pmt -n 3 -c 3 OrchidCncPistonDisp'),

 ('Use -r option for multiple runs, notice run after PowerOn also starts with PowerOn',
  'pmt -n 3 -r 2 OrchidCncPistonDisp')
]
