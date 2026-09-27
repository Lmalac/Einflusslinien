from model.beam import Beam, SupportType


def test_internal_hinge_dof_mapping():

    beam = Beam()

    beam.add_span(6.0)

    beam.add_support(0.0, SupportType.PINNED)
    beam.add_support(6.0, SupportType.ROLLER)

    beam.add_internal_hinge(3.0)

    print("\n=== НУМЕРАЦИЯ DOF С ШАРНИРОМ ===")

    print("Обычный узел:")
    print("  v  = 2*i")
    print("  θ  = 2*i + 1")

    print("\nШарнирный узел x = 3.0 м должен иметь:")
    print("  v       — общий")
    print("  θ_left  — отдельный")
    print("  θ_right — отдельный")

    hinge_node = 1

    v_dof = 2 * hinge_node
    theta_left_dof = 2 * hinge_node + 1
    theta_right_dof = 2 * hinge_node + 2

    print("\nПредварительная схема:")
    print(f"  v        = DOF {v_dof}")
    print(f"  θ_left   = DOF {theta_left_dof}")
    print(f"  θ_right  = DOF {theta_right_dof}")


if __name__ == "__main__":
    test_internal_hinge_dof_mapping()