import pint

from rezipe import Measure, recipe
from rezipe.wares import Pot
from rezipe.ingredients import RegularTofu, SnowPea, EnokiMushroom, DashiSoup, Miso

ureg  = pint.UnitRegistry()

class MisoSoup(Rezipe):
    """
    A simple miso soup by Rie
    """
    ref = "https://tasty.co/recipe/miso-soup"

    # kichenwares
    pot: Pot = Pot()

    # Ingredients
    dashi: DashiSoup = Measure(360 * ureg.mL)
    tofu: RegularTofu = Measure(200 * ureg.gram)
    pea: SnowPea = Measure(75 * ureg.gram)
    mushroom: EnokiMushroom = Measure(55 * ureg.gram)
    miso: Miso = Measure(2*ureg('tablespoon'))

    # can a decorator help to expose class variable
    @recipe
    async def make(self):
        # could we make local variable auto expose from class variable
        pot += dashi
        await pot.boil()

        # self assign inplace, is it even possible?
        await tofu.cut(style="cube")

        # method chaining async? possible with # https://stackoverflow.com/questions/28522999/method-chaining-with-asyncio-coroutines
        await pea.trim().cut(in="half")

        await mushroom.cut(remove="end")

        pot += tofu + pea + mushroom
        await pot.slimmer().for(3*ureg.min)

        assert pot.heat.isOff
        miso = await Miso(2*ureg('tablespoon')).dissolve(with=pot.soup)
        pot.add(miso)

        await pot.boil(progress=0.75)

        self.serve(pot)