

cd command
make clean_all
make 
make install
cd ..

make image
bochs -f bochsrc
