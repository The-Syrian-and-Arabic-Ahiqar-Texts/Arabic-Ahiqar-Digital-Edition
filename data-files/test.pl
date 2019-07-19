#!/usr/bin/perl

use utf8;

use Encode qw(decode encode); # ensures utf8 standards
use open ':encoding(utf8)'; #output in utf8 (else you get blocks)

#### DONT CHANGE ABOVE

# THIS IS YOUR SOURCE FILE
my $input = '\\winfs-uni.top.gwdg.de\aelrefa$\Dokumente\DFG AHIKAR PROJECT 2018\Arabic-Ahiqar-Digital-Edition\data-files\tei-files\Cod_Arabe_3637.tei'; #This is the location to the source or input file

#### READ FILE CONTENTS INTO THE COMPUTERS MEMORY
my $f = do {
    local $/ = undef;
    open my $fh, "$input" or die "Source file not found: $!";
    <$fh>;
};

$f =~ s{<w n="\d+">(.*?)</w>}{$1}g;
#$f =~ s{(حيقار)}{<persName>$1</persName>}g; # parens capture find. so use $1 or $2 or $3

#FIND AND REPLACE EXPRESSION (regex101.com)
#$f =~ s{}{}g;
#$f =~ s{}{}g;


# VALID LOCATION TO DESKTOP OR FOLDER
my $tagged = '\\\winfs-uni.top.gwdg.de\aelrefa$\test.tei'; #WHERE YOU WANT THE TAGGED FILE TO EXIST ON COMP


#DONT CHANGE ANY THING BELOW
open my $outfile, ">:utf8", "$tagged", or die "Cannot save file to the location of $tagged: $!";
print $outfile $f;
close($outfile);
print("The file was processed.");