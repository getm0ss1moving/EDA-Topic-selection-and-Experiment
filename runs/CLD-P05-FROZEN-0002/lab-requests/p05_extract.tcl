# Extract DMP results from pinned OpenSTA for the P3-P5 fixtures.
# Run: sta -no_init -no_splash -exit p05_extract.tcl  (cwd = fixture dir, env P05_OUT)
# Output raw.tsv records (times in seconds, as stored in the timing graph):
#   G net rf in_slew gate_delay drvr_slew report_text debug_text
#   W net rf load_pin wire_delay load_slew
read_liberty p05a.lib
read_liberty p05b.lib
read_verilog p05.v
link_design p05
read_spef p05.spef
source p05_inputs.tcl
source p05_nets.tcl
sta::find_delays
set corner [sta::cmd_corner]
set out [open "$env(P05_OUT)/raw.tsv" w]

proc flat { s } {
  return [string map [list "\n" " | " "\t" " "] $s]
}

foreach rec $p05_nets {
  lassign $rec net drv loads
  set apin [get_pins $drv/A]
  set zpin [get_pins $drv/Z]
  set av [lindex [$apin vertices] 0]
  set zv [lindex [$zpin vertices] 0]
  set zname [get_full_name $zpin]
  set iter [$av out_edge_iterator]
  while {[$iter has_next]} {
    set e [$iter next]
    if { [get_full_name [$e to_pin]] != $zname } { continue }
    foreach arc [$e timing_arcs] {
      set rf [$arc to_edge_name]
      set in_rf [$arc from_edge_name]
      set gd [$e arc_delay $arc $corner max]
      sta::set_debug dmp_ceff 3
      sta::redirect_string_begin
      set rpt [sta::report_delay_calc_cmd $e $arc $corner max 9]
      set dbg [sta::redirect_string_end]
      sta::set_debug dmp_ceff 0
      puts $out [join [list G $net $rf [$av slew $in_rf max] $gd [$zv slew $rf max] \
                         [flat $rpt] [flat $dbg]] "\t"]
    }
  }
  $iter finish
  set iter [$zv out_edge_iterator]
  while {[$iter has_next]} {
    set e [$iter next]
    if { [$e role] != "wire" } { continue }
    set lpin [$e to_pin]
    set lv [$e to]
    foreach arc [$e timing_arcs] {
      set rf [$arc to_edge_name]
      puts $out [join [list W $net $rf [get_full_name $lpin] \
                         [$e arc_delay $arc $corner max] [$lv slew $rf max]] "\t"]
    }
  }
  $iter finish
}
close $out
puts "p05_extract done: [llength $p05_nets] nets"
