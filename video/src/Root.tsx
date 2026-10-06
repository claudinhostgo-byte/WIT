import { Composition } from "remotion";
import { WitPresentacion, DURACION_TOTAL } from "./WitPresentacion";
import { WitVertical, DURACION_VERTICAL } from "./Vertical";
import { WitMicrosoftCloud, DURACION_MSCLOUD } from "./MicrosoftCloud";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="WitPresentacion"
      component={WitPresentacion}
      durationInFrames={DURACION_TOTAL}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="WitVertical"
      component={WitVertical}
      durationInFrames={DURACION_VERTICAL}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="MicrosoftCloudVertical"
      component={WitMicrosoftCloud}
      durationInFrames={DURACION_MSCLOUD}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="MicrosoftCloudFeed"
      component={WitMicrosoftCloud}
      durationInFrames={DURACION_MSCLOUD}
      fps={30}
      width={1080}
      height={1350}
    />
  </>
);
