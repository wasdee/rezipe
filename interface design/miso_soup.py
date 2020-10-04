import pint

from rezipe.kitchenware import Pot
from rezipe.ingredients import Tofu, SnowPea, EnokiMushroom, DashiSoup, Miso

ureg  = pint.UnitRegistry()

class MisoSoup(Rezipe):
    ref = "https://tasty.co/recipe/miso-soup"

    async def cook():
        pot = Pot()
        pot.add(DashiSoup(360 * ureg.mL))
        pot = await pot.boil()

        tofu = await Tofu(200 * ureg.gram).cut(style="cube")
        pea = await SnowPea(75 * ureg.gram).trim()
        pea = await pea.cut(in="half")
        mushroom = await EnokiMushroom(55 * ureg.gram).cut(remove="end")


        pot = pot.add(tofu, pea, mushroom)
        pot = await pot.slimmer().for(3*ureg.min)

        assert pot.heat.isOff
        miso = await Miso(2*ureg('tablespoon')).dissolve(with=pot.soup)
        pot.add(miso)

        pot = await pot.boil(progress=0.75)

        self.serve(pot)