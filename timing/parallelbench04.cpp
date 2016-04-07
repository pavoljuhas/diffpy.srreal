#include <boost/chrono.hpp>
#include <iostream>
#include <fstream>
#include <vector>
#include <diffpy/serialization.hpp>
#include <diffpy/srreal/PeriodicStructureAdapter.hpp>
#include <diffpy/srreal/PDFCalculator.hpp>

using namespace std;


int main()
{
    using namespace diffpy::srreal;
    using boost::archive::binary_iarchive;
    typedef boost::chrono::high_resolution_clock Time;
    StructureAdapterPtr adpt;
    ifstream fp("menthol.dump");
    binary_iarchive(fp) >> adpt;
    QuantityType rgrid, pdf;
    PDFCalculator pc;
    boost::chrono::duration<double> etime;

    Time::time_point t0 = Time::now();
    pc.setRmax(30);
    pc.setQmax(25);
    pc.eval(adpt);
    rgrid = pc.getRgrid();
    pdf = pc.getPDF();
    Time::time_point t1 = Time::now();
    etime = t1 - t0;
    cout << "elapsed wall time: " << etime.count() << '\n';
    return 0;
}
