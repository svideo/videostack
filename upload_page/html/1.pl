use File::Slurp qw(read_file);
use MIME::Base64;

my $filename = '/data1/speed/images/1.jpg';

my $bin = read_file( $filename,  binmode => ':raw'  ) ;
#
my $encode_str = "data:image/jpeg;base64," . encode_base64($bin);
print $encode_str;
#print "";


