import numpy
#https://riptutorial.com/algorithm/example/24981/introduction-to-dynamic-time-warping
#random data to test
#timeSeries1 data
#timeSeries2 data

#Find the difference in points
#diff = (x-y)^2
#Table[i][j] := d(i, j) + min(Table[i-1][j], Table[i-1][j-1], Table[i][j-1])
#Procedure DTW(Sample, Test):
#n := Sample.length
#m := Test.length
#Create Table[n + 1][m + 1]
#for i from 1 to n
#    Table[i][0] := infinity
#end for
#for i from 1 to m
#    Table[0][i] := infinity
#end for
#Table[0][0] := 0
#for i from 1 to n
#    for j from 1 to m
#        Table[i][j] := d(Sample[i], Test[j])
#                       + minimum(Table[i-1][j-1],      //match
#                                 Table[i][j-1],        //insertion
#                                 Table[i-1][j])        //deletion
#    end for
#end for
#Return Table[n + 1][m + 1]

#if Table[i-1][j-1] <= Table[i-1][j] and Table[i-1][j-1] <= Table[i][j-1]
#    i := i - 1
#    j := j - 1
#else if Table[i-1][j] <= Table[i-1][j-1] and Table[i-1][j] <= Table[i][j-1]
#    i := i - 1
#else
#    j := j - 1
#end if