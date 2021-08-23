#!/usr/bin/env perl
use warnings 'all';
use strict;
use autodie;

#temp
no warnings 'once';

my $root = "/sys/bus/usb/devices";
opendir(D, $root) || die "Can't open directory: $!\n";
while (my $f = readdir(D)) {#loop through all USB devices
	if($f =~ /^\d.*/){
		my $path = "$root/$f/product";
		if(-f $path){
			open(my $yourhandle, '<', $path)
    			or die "Unable to open file, $!";
    		while (<$yourhandle>) { # Read the file line per line
			   if ($_ =~ /.*(Mouse|Keyboard|Receiver|LAN).*/){#test to see if mouse, keyboard, some sort of reciver, or internet
					my $filename = "$root/$f/power/control";#turn off optimizations
					open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
					print $fh "on";
					close $fh;
					print "Turned off power optimization for $_";
			   }
			}
    		close($yourhandle)
    			or warn "Unable to close the file handle: $!";
		}

	}
    #print "\$f = $f\n";
}
closedir(D);
