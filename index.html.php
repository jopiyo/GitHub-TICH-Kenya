<?php
/**
 * ClimateGuard Simulation Script (Color-Coded Web UI)
 * Developed for Till Africa POS - Health Informatics Framework
 */

class ClimateGuardSimulation {
    private $region;
    private $rainfallMm;
    private $tempCelsius;
    private $healthFacilityCapacity; // Scale of 1 (Low) to 5 (High)

    public function __construct($region, $rainfallMm, $tempCelsius, $healthFacilityCapacity) {
        $this->region = $region;
        $this->rainfallMm = $rainfallMm;
        $this->tempCelsius = $tempCelsius;
        $this->healthFacilityCapacity = $healthFacilityCapacity;
    }

    public function predictOutbreaks() {
        $risks = [];

        if ($this->rainfallMm > 150 && $this->tempCelsius > 24) {
            $risks['Malaria'] = ['Level' => 'HIGH', 'Score' => 85, 'Reason' => 'Optimal breeding conditions for vectors due to heavy rainfall and warmth.'];
        } else {
            $risks['Malaria'] = ['Level' => 'MODERATE', 'Score' => 45, 'Reason' => 'Normal baseline vector activity.'];
        }

        if ($this->rainfallMm > 200) {
            $risks['Cholera'] = ['Level' => 'CRITICAL', 'Score' => 92, 'Reason' => 'Severe flooding risk and potential water source contamination.'];
        } elseif ($this->rainfallMm > 100) {
            $risks['Cholera'] = ['Level' => 'MODERATE', 'Score' => 50, 'Reason' => 'Elevated surface runoff.'];
        } else {
            $risks['Cholera'] = ['Level' => 'LOW', 'Score' => 15, 'Reason' => 'Stable water sanitation conditions.'];
        }

        if ($this->tempCelsius > 26 && $this->rainfallMm > 120) {
            $risks['Dengue'] = ['Level' => 'HIGH', 'Score' => 78, 'Reason' => 'Accelerated mosquito lifecycle in warm, wet conditions.'];
        } else {
            $risks['Dengue'] = ['Level' => 'LOW', 'Score' => 30, 'Reason' => 'Temperature and rainfall below peak transmission threshold.'];
        }

        return $risks;
    }

    public function evaluateEWS($risks) {
        $alerts = [];
        foreach ($risks as $disease => $data) {
            if ($data['Level'] === 'HIGH' || $data['Level'] === 'CRITICAL') {
                $alerts[] = [
                    'Channel' => 'SMS / USSD Gateway',
                    'Recipient' => 'Community Health Volunteers (CHVs) & Facility Managers in ' . $this->region,
                    'Message' => "ALERT: {$disease} outbreak risk is {$data['Level']} ({$data['Score']}%) in {$this->region}. Rainfall: {$this->rainfallMm}mm, Temp: {$this->tempCelsius}°C. Initiate community surveillance."
                ];
            }
        }
        return $alerts;
    }

    public function assessVulnerability($risks) {
        $maxScore = max(array_column($risks, 'Score'));
        $isHotspot = ($maxScore > 70 && $this->healthFacilityCapacity <= 2);
        
        return [
            'IsHotspot' => $isHotspot,
            'VulnerabilityIndex' => $isHotspot ? 'CRITICAL HOTSPOT' : 'STABLE / MANAGABLE',
            'FacilityCapacityScore' => $this->healthFacilityCapacity
        ];
    }

    public function getResourceRecommendations($risks) {
        $recommendations = [];
        foreach ($risks as $disease => $data) {
            if ($data['Score'] > 70) {
                if ($disease === 'Malaria') {
                    $recommendations[] = "Preposition 500 courses of Artemisinin-based Combination Therapies (ACTs) and Long-Lasting Insecticidal Nets (LLINs).";
                }
                if ($disease === 'Cholera') {
                    $recommendations[] = "Preposition 200 water treatment kits (Aquatabs), Oral Rehydration Salts (ORS), and chlorine dispensers.";
                }
                if ($disease === 'Dengue') {
                    $recommendations[] = "Deploy larvicides and launch community awareness campaigns on stagnant water clearance.";
                }
            }
        }
        if (empty($recommendations)) {
            $recommendations[] = "Maintain standard buffer stocks; no emergency prepositioning required.";
        }
        return $recommendations;
    }

    public function runSimulation() {
        $risks = $this->predictOutbreaks();
        $vuln = $this->assessVulnerability($risks);
        $alerts = $this->evaluateEWS($risks);
        $supplies = $this->getResourceRecommendations($risks);

        // Styling status colors
        $statusColor = $vuln['IsHotspot'] ? '#d9534f' : '#5cb85c'; // Red for Hotspot, Green for Stable

        echo "<div style='font-family: Arial, sans-serif; max-width: 900px; margin: 30px auto; background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>";
        echo "<h2 style='color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px;'>🌍 CLIMATEGUARD SIMULATION ENGINE - TILL AFRICA POS</h2>";
        
        echo "<p><strong>Region Target:</strong> {$this->region}<br>";
        echo "<strong>Meteorological Input:</strong> Rainfall = {$this->rainfallMm} mm | Temp = {$this->tempCelsius} °C<br>";
        echo "<strong>Health Facility Capacity Index:</strong> {$this->healthFacilityCapacity}/5</p>";

        // [1] Predictions
        echo "<h3 style='color: #34495e;'>[1] Predictive Disease Modeling</h3>";
        echo "<ul>";
        foreach ($risks as $disease => $info) {
            $badgeColor = ($info['Level'] === 'HIGH' || $info['Level'] === 'CRITICAL') ? '#d9534f' : '#f0ad4e';
            echo "<li><strong>{$disease}:</strong> <span style='background: {$badgeColor}; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 12px;'>{$info['Level']} ({$info['Score']}%)</span><br><small>{$info['Reason']}</small></li><br>";
        }
        echo "</ul>";

        // [2] Vulnerability
        echo "<h3 style='color: #34495e;'>[2] Vulnerability Mapping & Hotspot Analysis</h3>";
        echo "<p><strong>Status:</strong> <span style='color: #fff; background: {$statusColor}; padding: 4px 10px; border-radius: 4px; font-weight: bold;'>{$vuln['VulnerabilityIndex']}</span></p>";
        echo "<p><strong>Hotspot Flag:</strong> " . ($vuln['IsHotspot'] ? '<span style="color: #d9534f; font-weight: bold;">YES (High Climate Risk Intersecting Low Health Capacity)</span>' : '<span style="color: #5cb85c; font-weight: bold;">NO</span>') . "</p>";

        // [3] EWS
        echo "<h3 style='color: #34495e;'>[3] Early Warning System (SMS / USSD Dispatch)</h3>";
        if (!empty($alerts)) {
            foreach ($alerts as $alert) {
                echo "<div style='background: #fdf7f7; border-left: 4px solid #d9534f; padding: 10px; margin-bottom: 10px;'>";
                echo "<strong>[DISPATCHED via {$alert['Channel']}]</strong><br>";
                echo "<small>To: {$alert['Recipient']}</small><br>";
                echo "<em>\"{$alert['Message']}\"</em>";
                echo "</div>";
            }
        } else {
            echo "<p style='color: #5cb85c;'>Thresholds normal. No emergency SMS alerts triggered.</p>";
        }

        // [4] Resources
        echo "<h3 style='color: #34495e;'>[4] Resource Optimization & Supply Prepositioning</h3>";
        echo "<ul>";
        foreach ($supplies as $supply) {
            echo "<li>{$supply}</li>";
        }
        echo "</ul>";

        echo "</div>";
    }
}

// Execute test drive simulation
$simulation = new ClimateGuardSimulation(
    region: "Mageta Island / Lake Victoria Basin", 
    rainfallMm: 210,   
    tempCelsius: 27.5, 
    healthFacilityCapacity: 2 
);

$simulation->runSimulation();
?>