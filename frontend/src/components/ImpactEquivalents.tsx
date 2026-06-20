import { Car, Lightbulb, Smartphone, TreePine } from 'lucide-react';
import { Card, CardContent } from './ui/card';

interface EquivalentsData {
  driving_km?: number;
  smartphone_charges?: number;
  trees_to_offset?: number;
  led_bulb_hours?: number;
}

export function ImpactEquivalents({ data }: { data: EquivalentsData }) {
  if (!data) return null;

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <Card className="bg-slate-900/50 border-slate-800">
        <CardContent className="p-4 flex flex-col items-center text-center">
          <div className="p-3 bg-blue-500/10 rounded-full mb-3">
            <Car className="w-6 h-6 text-blue-500" />
          </div>
          <p className="text-2xl font-bold text-slate-200">{data.driving_km?.toLocaleString()}</p>
          <p className="text-xs text-slate-400 mt-1">km driven in a car</p>
        </CardContent>
      </Card>
      
      <Card className="bg-slate-900/50 border-slate-800">
        <CardContent className="p-4 flex flex-col items-center text-center">
          <div className="p-3 bg-emerald-500/10 rounded-full mb-3">
            <TreePine className="w-6 h-6 text-emerald-500" />
          </div>
          <p className="text-2xl font-bold text-slate-200">{data.trees_to_offset?.toLocaleString()}</p>
          <p className="text-xs text-slate-400 mt-1">trees needed to offset</p>
        </CardContent>
      </Card>

      <Card className="bg-slate-900/50 border-slate-800">
        <CardContent className="p-4 flex flex-col items-center text-center">
          <div className="p-3 bg-purple-500/10 rounded-full mb-3">
            <Smartphone className="w-6 h-6 text-purple-500" />
          </div>
          <p className="text-2xl font-bold text-slate-200">{data.smartphone_charges?.toLocaleString()}</p>
          <p className="text-xs text-slate-400 mt-1">smartphone charges</p>
        </CardContent>
      </Card>

      <Card className="bg-slate-900/50 border-slate-800">
        <CardContent className="p-4 flex flex-col items-center text-center">
          <div className="p-3 bg-amber-500/10 rounded-full mb-3">
            <Lightbulb className="w-6 h-6 text-amber-500" />
          </div>
          <p className="text-2xl font-bold text-slate-200">{data.led_bulb_hours?.toLocaleString()}</p>
          <p className="text-xs text-slate-400 mt-1">LED bulb hours</p>
        </CardContent>
      </Card>
    </div>
  );
}
