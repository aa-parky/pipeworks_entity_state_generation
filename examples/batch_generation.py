"""Batch Generation Example for Pipeworks Conditional Axis.

This example demonstrates efficient bulk generation of entities:
- Generating large batches of complete entities
- Exporting to various formats (JSON, CSV, dict)
- Filtering and selecting from generated batches
- Memory-efficient streaming generation
- Performance considerations for large-scale generation

Run this example:
    python examples/batch_generation.py
"""

import csv
import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from condition_axis import (
    generate_condition,
    generate_occupation_condition,
    condition_to_prompt,
    occupation_condition_to_prompt,
)


def generate_entity(seed: int) -> dict[str, Any]:
    """Generate a complete entity with all three condition systems.

    Args:
        seed: Random seed for reproducible generation.

    Returns:
        Dictionary containing seed and all three condition types.

    Example:
        >>> entity = generate_entity(42)
        >>> entity['seed']
        42
        >>> 'character' in entity
        True
    """
    return {
        "seed": seed,
        "character": generate_condition(seed=seed),
        "facial": {"facial_signal": generate_condition(seed=seed).get("facial_signal", "")},
        "occupation": generate_occupation_condition(seed=seed),
    }


def generate_batch(start_seed: int, count: int) -> list[dict[str, Any]]:
    """Generate a batch of complete entities.

    Args:
        start_seed: Starting seed value.
        count: Number of entities to generate.

    Returns:
        List of entity dictionaries.

    Example:
        >>> batch = generate_batch(0, 10)
        >>> len(batch)
        10
        >>> batch[0]['seed']
        0
    """
    return [generate_entity(start_seed + i) for i in range(count)]


def generate_streaming(start_seed: int, count: int) -> Iterator[dict[str, Any]]:
    """Generate entities one at a time for memory efficiency.

    This generator yields entities one at a time rather than creating
    a full list, which is useful for very large batches that might
    not fit in memory.

    Args:
        start_seed: Starting seed value.
        count: Number of entities to generate.

    Yields:
        Entity dictionaries one at a time.

    Example:
        >>> for entity in generate_streaming(0, 5):
        ...     print(entity['seed'])
        0
        1
        2
        3
        4
    """
    for i in range(count):
        yield generate_entity(start_seed + i)


def example_1_simple_batch_generation() -> None:
    """Demonstrate generating a simple batch of entities.

    This is the most straightforward approach for moderate batch sizes
    (up to a few thousand entities).
    """
    print("=" * 70)
    print("EXAMPLE 1: Simple Batch Generation")
    print("=" * 70)

    batch_size = 20
    print(f"\nGenerating {batch_size} entities...")

    batch = generate_batch(start_seed=0, count=batch_size)

    print(f"Generated {len(batch)} entities\n")
    print("First 5 entities:")

    for entity in batch[:5]:
        seed = entity["seed"]
        char_prompt = condition_to_prompt(entity["character"])
        face_prompt = condition_to_prompt(entity["facial"])
        occ_prompt = occupation_condition_to_prompt(entity["occupation"])

        full_prompt = f"{char_prompt}, {face_prompt}, {occ_prompt}"
        print(f"  Entity #{seed}: {full_prompt}")


def example_2_export_to_json() -> None:
    """Demonstrate exporting a batch to JSON format.

    JSON is ideal for:
    - Structured data interchange
    - API responses
    - Configuration files
    - Human-readable storage
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Export to JSON")
    print("=" * 70)

    batch = generate_batch(start_seed=100, count=5)

    # Prepare for JSON serialization
    json_data = {
        "metadata": {
            "generator": "pipeworks-conditional-axis",
            "version": "1.0.0",
            "start_seed": 100,
            "count": 5,
        },
        "entities": batch,
    }

    # Convert to JSON string
    json_output = json.dumps(json_data, indent=2)

    print("\nJSON Output (first 500 characters):")
    print(json_output[:500] + "...")

    # Optionally save to file
    # output_path = Path("entities.json")
    # output_path.write_text(json_output)
    # print(f"\nSaved to: {output_path}")


def example_3_export_to_csv() -> None:
    """Demonstrate exporting a batch to CSV format.

    CSV is ideal for:
    - Spreadsheet analysis
    - Database imports
    - Data science workflows
    - Simple tabular data
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Export to CSV")
    print("=" * 70)

    batch = generate_batch(start_seed=200, count=10)

    # Flatten entities for CSV (one row per entity)
    csv_rows = []
    for entity in batch:
        char = entity["character"]
        facial = entity["facial"]
        occ = entity["occupation"]

        row = {
            "seed": entity["seed"],
            # Character axes
            "physique": char.get("physique", ""),
            "wealth": char.get("wealth", ""),
            "health": char.get("health", ""),
            "demeanor": char.get("demeanor", ""),
            "age": char.get("age", ""),
            # Facial axes
            "overall_impression": facial.get("overall_impression", ""),
            # Occupation axes
            "legitimacy": occ.get("legitimacy", ""),
            "visibility": occ.get("visibility", ""),
            "moral_load": occ.get("moral_load", ""),
            "dependency": occ.get("dependency", ""),
            "risk_exposure": occ.get("risk_exposure", ""),
            # Combined prompt
            "full_prompt": (
                f"{condition_to_prompt(char)}, "
                f"{condition_to_prompt(facial)}, "
                f"{occupation_condition_to_prompt(occ)}"
            ),
        }
        csv_rows.append(row)

    # Display as table
    print("\nCSV Preview (first 3 rows):\n")
    print(f"{'seed':<6} {'physique':<10} {'wealth':<12} {'legitimacy':<12} {'visibility':<12}")
    print("-" * 70)

    for row in csv_rows[:3]:
        print(
            f"{row['seed']:<6} {row['physique']:<10} {row['wealth']:<12} "
            f"{row['legitimacy']:<12} {row['visibility']:<12}"
        )

    # Optionally save to file
    # output_path = Path("entities.csv")
    # with output_path.open("w", newline="") as csvfile:
    #     fieldnames = csv_rows[0].keys()
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerows(csv_rows)
    # print(f"\nSaved to: {output_path}")


def example_4_filtering_and_selection() -> None:
    """Demonstrate filtering generated entities by criteria.

    Generate a large batch and select entities that match specific
    requirements. This is useful for finding entities with desired
    characteristics.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Filtering and Selection")
    print("=" * 70)

    batch_size = 100
    print(f"\nGenerating {batch_size} entities for filtering...")

    batch = generate_batch(start_seed=0, count=batch_size)

    # Filter 1: Find wealthy individuals
    wealthy = [e for e in batch if e["character"].get("wealth") in ["wealthy", "decadent"]]

    print(f"\nFilter 1: Wealthy individuals")
    print(f"  Found: {len(wealthy)} / {batch_size} ({len(wealthy)/batch_size*100:.1f}%)")
    if wealthy:
        example = wealthy[0]
        prompt = (
            f"{condition_to_prompt(example['character'])}, "
            f"{condition_to_prompt(example['facial'])}, "
            f"{occupation_condition_to_prompt(example['occupation'])}"
        )
        print(f"  Example (seed {example['seed']}): {prompt}")

    # Filter 2: Find illicit occupations
    illicit = [e for e in batch if e["occupation"].get("legitimacy") == "illicit"]

    print(f"\nFilter 2: Illicit occupations")
    print(f"  Found: {len(illicit)} / {batch_size} ({len(illicit)/batch_size*100:.1f}%)")
    if illicit:
        example = illicit[0]
        prompt = (
            f"{condition_to_prompt(example['character'])}, "
            f"{condition_to_prompt(example['facial'])}, "
            f"{occupation_condition_to_prompt(example['occupation'])}"
        )
        print(f"  Example (seed {example['seed']}): {prompt}")

    # Filter 3: Complex criteria - young and weathered
    young_weathered = [
        e
        for e in batch
        if e["character"].get("age") == "young"
        and e["facial"].get("overall_impression") == "weathered"
    ]

    print(f"\nFilter 3: Young but weathered (complex criteria)")
    print(
        f"  Found: {len(young_weathered)} / {batch_size} "
        f"({len(young_weathered)/batch_size*100:.1f}%)"
    )
    if young_weathered:
        example = young_weathered[0]
        prompt = (
            f"{condition_to_prompt(example['character'])}, "
            f"{condition_to_prompt(example['facial'])}, "
            f"{occupation_condition_to_prompt(example['occupation'])}"
        )
        print(f"  Example (seed {example['seed']}): {prompt}")


def example_5_memory_efficient_streaming() -> None:
    """Demonstrate memory-efficient streaming generation.

    For very large batches (10,000+), streaming generation avoids
    loading all entities into memory at once.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Memory-Efficient Streaming")
    print("=" * 70)

    large_batch_size = 1000
    print(f"\nGenerating {large_batch_size} entities via streaming...")

    # Count specific conditions without storing all entities
    wealthy_count = 0
    illicit_count = 0
    young_count = 0

    for entity in generate_streaming(start_seed=0, count=large_batch_size):
        if entity["character"].get("wealth") in ["wealthy", "decadent"]:
            wealthy_count += 1
        if entity["occupation"].get("legitimacy") == "illicit":
            illicit_count += 1
        if entity["character"].get("age") == "young":
            young_count += 1

    print(f"\nStatistics from {large_batch_size} entities:")
    print(f"  Wealthy: {wealthy_count} " f"({wealthy_count/large_batch_size*100:.1f}%)")
    print(f"  Illicit: {illicit_count} " f"({illicit_count/large_batch_size*100:.1f}%)")
    print(f"  Young: {young_count} ({young_count/large_batch_size*100:.1f}%)")

    print(f"\nMemory benefit: Processed {large_batch_size} entities " "without storing them all")


def example_6_parallel_generation_pattern() -> None:
    """Demonstrate pattern for parallel generation (conceptual).

    For extremely large batches, you might want to use parallel
    processing. This example shows the pattern (without actual
    multiprocessing for simplicity).
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Parallel Generation Pattern")
    print("=" * 70)

    total_entities = 1000
    num_workers = 4
    entities_per_worker = total_entities // num_workers

    print(f"\nConcept: Generate {total_entities} entities using {num_workers} workers")
    print(f"Each worker generates {entities_per_worker} entities\n")

    # Simulate worker assignments
    workers = []
    for worker_id in range(num_workers):
        start_seed = worker_id * entities_per_worker
        end_seed = start_seed + entities_per_worker - 1
        workers.append(
            {
                "worker_id": worker_id,
                "start_seed": start_seed,
                "end_seed": end_seed,
                "count": entities_per_worker,
            }
        )

    print("Worker assignments:")
    for worker in workers:
        print(
            f"  Worker {worker['worker_id']}: "
            f"seeds {worker['start_seed']}-{worker['end_seed']} "
            f"({worker['count']} entities)"
        )

    print("\nImplementation pattern:")
    print(
        """
    # Using Python's multiprocessing:
    from multiprocessing import Pool

    def worker_task(args):
        start_seed, count = args
        return generate_batch(start_seed, count)

    with Pool(processes=4) as pool:
        tasks = [(w['start_seed'], w['count']) for w in workers]
        results = pool.map(worker_task, tasks)
        all_entities = [e for batch in results for e in batch]
    """
    )


def main() -> None:
    """Run all batch generation examples.

    This main function executes all examples demonstrating efficient
    bulk generation, export formats, filtering, and performance
    optimization strategies.
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PIPEWORKS CONDITIONAL AXIS" + " " * 27 + "║")
    print("║" + " " * 18 + "BATCH GENERATION EXAMPLES" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")

    example_1_simple_batch_generation()
    example_2_export_to_json()
    example_3_export_to_csv()
    example_4_filtering_and_selection()
    example_5_memory_efficient_streaming()
    example_6_parallel_generation_pattern()

    print("\n" + "=" * 70)
    print("All batch generation examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  - Simple batch generation for moderate sizes (< 10k)")
    print("  - Export to JSON for structured data interchange")
    print("  - Export to CSV for spreadsheet/database workflows")
    print("  - Filter large batches to find desired characteristics")
    print("  - Use streaming for memory-efficient large batches")
    print("  - Consider parallel processing for very large batches")
    print("\nNext Steps:")
    print("  - Try custom_axes.py to extend the system with new axes")
    print("  - Try image_prompt_generation.py for visual AI integration")
    print("  - See integration_example.py for combining all systems")
    print()


if __name__ == "__main__":
    main()
