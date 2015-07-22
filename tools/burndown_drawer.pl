use GD::Graph::lines;
use utf8;

my @data = ( 
    ["start", "7.22", "7.23", "7.24", "7.25", "7.27", "7.28", "7.29", "7.30", "7.31", "8.1", "8.3", "8.4"],
    [ 171, 171, 171, 171, 171, 171, 171, 171, 171, 171, 171, 171, 171],
    [ 171, 156.75, 142.5, 128.25, 114, 99.75, 85.5,71.25, 57, 42.75, 28.5, 14.25, 0],
);

my $graph = GD::Graph::lines->new(800, 600);

$graph->set( 
    dclrs             => [ qw(cyan black) ],
    line_width        => 6,
    x_label           => 'Date',
    x_label_position  => 1/2,
    y_label           => 'Workload(Man-Hour)',
    y_number_format   => sub { return int(shift); },
    title             => 'Second Round (7.22~8.5) Burndown',
    y_max_value       => 185.25,
    y_tick_number     => 171/12,
    y_label_skip      => 1,
) or die $graph->error;

my $gd = $graph->plot(\@data) or die $graph->error;
open(IMG, '>file.png') or die $!;
binmode IMG;
print IMG $gd->png;
