use GD::Graph::lines;
use utf8;

my @data = ( 
    ["start", "8.5", "8.6", "8.7", "8.8", "8.10", "8.11", "8.12", "8.13", "8.14", "8.15", "8.17", "8.18"],
    [ 199, 179, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 199, 182.5, 166, 149.5, 133, 116.5, 100, 83.5, 67, 50.5, 34, 17.5, 0],
);

my $graph = GD::Graph::lines->new(800, 600);

$graph->set( 
    dclrs             => [ qw(black cyan) ],
    line_width        => 6,
    x_label           => 'Date',
    x_label_position  => 1/2,
    y_label           => 'Workload(Man-Hour)',
    y_number_format   => sub { return int(shift); },
    title             => 'Second Round (8.5~8.18) Burndown',
    y_max_value       => 199,
    y_tick_number     => 199/12,
    y_label_skip      => 1,
) or die $graph->error;

my $gd = $graph->plot(\@data) or die $graph->error;
open(IMG, '>file.png') or die $!;
binmode IMG;
print IMG $gd->png;
